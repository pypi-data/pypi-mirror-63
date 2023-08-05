#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Parse the FRC drive station logs which are packed binary data

# Notes on comparison to DSLog-Parse:
# D-P has packet_loss as a *signed* integer, which makes no sense. Unsigned looks sensible.
# D-P did not reverse the PDP values as was indicated in the CD post

import datetime
import math
import re
import struct

import bitstring


MAX_INT64 = 2**63 - 1
DSLOG_TIMESTEP = 0.020


def read_timestamp(strm):
    # Time stamp: int64, uint64
    b1 = strm.read(8)
    b2 = strm.read(8)
    if not b1 or not b2:
        return None
    sec = struct.unpack('>q', b1)[0]
    millisec = struct.unpack('>Q', b2)[0]

    # for now, ignore
    dt = datetime.datetime(1904, 1, 1, 0, 0, 0, tzinfo=datetime.timezone.utc)
    dt += datetime.timedelta(seconds=(sec + float(millisec) / MAX_INT64))
    return dt


class DSLogParser():
    def __init__(self, input_file):
        self.strm = open(input_file, 'rb')

        self.record_time_offset = datetime.timedelta(seconds=DSLOG_TIMESTEP)
        self.curr_time = None

        self.read_header()
        return

    def close(self):
        self.strm.close()
        return

    def read_records(self):
        if self.version != 3:
            raise Exception("Unknown file version number {}".format(self.version))

        while True:
            r = self.read_record_v3()
            if r is None:
                break
            yield r
        return

    def read_header(self):
        self.version = struct.unpack('>i', self.strm.read(4))[0]
        if self.version != 3:
            raise Exception("Unknown file version number {}".format(self.version))

        self.curr_time = read_timestamp(self.strm)
        return

    def read_record_v3(self):
        data_bytes = self.strm.read(10)
        if not data_bytes or len(data_bytes) < 10:
            return None
        pdp_bytes = self.strm.read(25)
        if not pdp_bytes or len(pdp_bytes) < 25:
            # should not happen!!
            raise EOFError("No data for PDP. Unexpected end of file.")

        res = {'time': self.curr_time}
        res.update(self.parse_data_v3(data_bytes))
        res.update(self.parse_pdp_v3(pdp_bytes))
        self.curr_time += self.record_time_offset
        return res

    @staticmethod
    def shifted_float(raw_value, shift_right):
        return raw_value / (2.0**shift_right)

    @staticmethod
    def unpack_bits(raw_value):
        '''Unpack and invert the bits in a byte'''

        status_bits = bitstring.Bits(bytes=raw_value)
        # invert them all
        return [not b for b in status_bits]

    @staticmethod
    def uint_from_bytes(bytes, offset, size_in_bits):
        '''Pull out an unsigned int from an array of bytes, with arbitrary bit start and length'''

        first_byte = math.floor(offset / 8)
        num_bytes = math.ceil(size_in_bits / 8)

        if num_bytes == 1:
            uint = struct.unpack_from('>B', bytes, first_byte)[0]
        elif num_bytes == 2:
            uint = struct.unpack_from('>H', bytes, first_byte)[0]
        else:
            # not needed here, and general case is harder
            raise Exception('not supported')

        # Need to mask off the incorrect high bits and then shift right to get rid of the incorrect low bits
        left_bitshift = offset - first_byte * 8
        right_bitshift = num_bytes * 8 - size_in_bits - left_bitshift

        return (uint & (0xFFFF >> left_bitshift)) >> right_bitshift

    def parse_data_v3(self, data_bytes):
        raw_values = struct.unpack('>BBHBcBBH', data_bytes)
        status_bits = self.unpack_bits(raw_values[4])

        res = {
            'round_trip_time': self.shifted_float(raw_values[0], 1),
            'packet_loss': 0.04 * raw_values[1],             # not shifted
            'voltage': self.shifted_float(raw_values[2], 8),
            'rio_cpu': 0.01 * self.shifted_float(raw_values[3], 1),
            'can_usage': 0.01 * self.shifted_float(raw_values[5], 1),
            'wifi_db': self.shifted_float(raw_values[6], 1),
            'bandwidth': self.shifted_float(raw_values[7], 8),

            'robot_disabled': status_bits[7],
            'robot_auto': status_bits[6],
            'robot_tele': status_bits[5],
            'ds_disabled': status_bits[4],
            'ds_auto': status_bits[3],
            'ds_tele': status_bits[2],
            'watchdog': status_bits[1],
            'brownout': status_bits[0],
        }

        return res

    def parse_pdp_v3(self, pdp_bytes):
        # from CD post https://www.chiefdelphi.com/forums/showpost.php?p=1556451&postcount=11
        # pdp_offsets = (8, 18, 28, 38, 52, 62, 72, 82, 92, 102, 116, 126, 136, 146, 156, 166)

        # from DSLog-Reader
        # these make more sense in terms of defining a packing scheme, so stick with them
        # looks like this is a 64-bit int holding 6 10-bit numbers and they ignore the extra 4 bits
        pdp_offsets = (8, 18, 28, 38, 48, 58,
                       72, 82, 92, 102, 112, 122,
                       136, 146, 156, 166)

        vals = []
        for offset in pdp_offsets:
            vals.append(self.shifted_float(self.uint_from_bytes(pdp_bytes, offset, 10), 3))

        # values are 15 through 0, so reverse the list
        # note: DSLog-Reader did not reverse these. Don't know who to believe.
        vals.reverse()

        total_i = 0.0
        for i in vals:
            total_i += i

        # the scaling on R, V and T are almost certainly not correct
        # need to find a reference for those values
        res = {
            'pdp_id': self.uint_from_bytes(pdp_bytes, 0, 8),
            'pdp_currents': vals,
            'pdp_resistance': self.uint_from_bytes(pdp_bytes, 176, 8),
            'pdp_voltage': self.uint_from_bytes(pdp_bytes, 184, 8),
            'pdp_temp': self.uint_from_bytes(pdp_bytes, 192, 8),
            'pdp_total_current': total_i,
        }

        return res


class DSEventParser():
    def __init__(self, input_file):
        self.strm = open(input_file, 'rb')
        self.version = None
        self.start_time = None

        self.read_header()
        return

    def close(self):
        self.strm.close()
        return

    def read_records(self):
        if self.version != 3:
            raise Exception("Unknown file version number {}".format(self.version))

        while True:
            r = self.read_record_v3()
            if r is None:
                break
            yield r
        return

    def read_header(self):
        self.version = struct.unpack('>i', self.strm.read(4))[0]
        if self.version != 3:
            raise Exception("Unknown file version number {}".format(self.version))
        self.start_time = read_timestamp(self.strm)  # file starttime
        return

    def read_record_v3(self):
        t = read_timestamp(self.strm)
        if t is None:
            return None

        msg_len = struct.unpack('>i', self.strm.read(4))[0]
        msg = struct.unpack('%ds' % msg_len, self.strm.read(msg_len))[0]
        msg = msg.decode('ascii', "backslashreplace")

        return {'time': t, 'message': msg}

    @staticmethod
    def find_match_info(filename):
        rdr = DSEventParser(filename)
        try:
            for rec in rdr.read_records():
                m = re.match(r'FMS Connected:\s+(?P<match>.*),\s+Field Time:\s+(?P<time>[0-9/ :]*)', rec['message'])
                if m:
                    return {'match_name': m.group('match'),
                            'field_time': datetime.datetime.strptime(m.group('time'), '%y/%m/%d %H:%M:%S')}
        finally:
            rdr.close()
        return None

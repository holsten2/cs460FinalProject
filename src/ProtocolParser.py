import re
import struct

from os import urandom
from random import randint

PROTOCOL_SEARCH_START = '[protocol:{}'
PROTOCOL_SEARCH_END = '[protocol:'
CLIENT = 'client'
SERVER = 'server'

PARSE_DATA_ARGS = {
    'string(': lambda x: bytes(x[8:-2], 'ASCII'),
    'repbyte(': lambda x: bytes([int(x[8:x.index(',')])] * int(x[x.index(',')+1:-1])),
    'randint(': lambda x: struct.pack('>I', randint(int(x[8:x.index(',')]), int(x[x.index(',')+1:-1]))),
    'random(': lambda x: urandom(int(x[7:-1])),  # change to urandom later
    'byte(': lambda x: bytes([int(x[5:-1])]),
    'int(': lambda x: struct.pack('>I', int(x[4:-1])),
}

REGEX_ENTRIES = [
    ('string', '\(".*?"\)'),
    ('prevmsg', '\(.*?\)'),
    ('repbyte', '\(.*?\)'),
    ('randint', '\(.*?\)'),
    ('random', '\(.*?\)'),
    ('byte', '\(.*?\)'),
    ('int', '\(.*?\)'),
]

PROTOCOL_SPLITTER = re.compile('|'.join(x + y for x, y in REGEX_ENTRIES))

class ProtocolParser:

    def __init__(self, protocol):
        self.repeat = 10
        self.protocol = protocol
        self.parsing_flag = False
    
    def parse_prevmsg(self, prev_msg2, args):
        offset = int(args[8:args.index(',')])
        length = int(args[args.index(',')+1:-1])
        # print(prev_msg2)
        # print(offset)
        # print(length)
        # print(prevmsg[offset:offset+length])
        # print('arght')
        return self.prevmsg[offset:offset+length]

    def parse_protocol_script(self, command, prev_msg2):
        if command.startswith(CLIENT) or command.startswith(SERVER):
            payload = re.findall(PROTOCOL_SPLITTER, command)
            output = []

            for p in payload:
                output.append(p)

            couple = ' '.join(output)
            commandType = "";
            #assert(CLIENT + ' send ' + couple + '\n' == command or SERVER + ' send ' + couple + '\n' == command)
            if(command.startswith(CLIENT)):
                commandType = CLIENT
            else:
                commandType = SERVER

            output_bytes = []

            for o in output:
                why = o[:o.index('(')+1]

                if why == 'prevmsg(':
                    b = self.parse_prevmsg(prev_msg2, o)
                else:
                    b = PARSE_DATA_ARGS[why](o)

                if type(b) is bytes:
                    output_bytes.append(b)
                # if len(str(b)) < 100:
                #     print(why[:-1] + ' ' + str(b))

            mall = b''.join(output_bytes)

            # if len(mall) < 300:
            #     print(mall)

            # print(len(mall))
            # print()
            return (commandType, mall)

    def parse_commands_from_file(self, path):
        with open(path, 'r') as spec_file:
            protocol_start = PROTOCOL_SEARCH_START.format(self.protocol)
            self.prevmsg = b''
            self.commands = [];

            for line in spec_file:
                if self.parsing_flag:
                    if line.startswith(PROTOCOL_SEARCH_END):
                        break
                    parsed_command = self.parse_protocol_script(line, self.prevmsg);
                    if(parsed_command): 
                        self.prevmsg = parsed_command[1]
                        self.commands.append(parsed_command)
                    else:
                        self.prevmsg = None;

                elif line.startswith(protocol_start):
                    self.parsing_flag = True

            return self.commands

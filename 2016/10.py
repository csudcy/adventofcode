INPUT = open('10.txt').read().strip()


class Bot(object):
    def __init__(self, botnet, id, output_low, output_high):
        self._botnet = botnet
        self._id = id
        # (type, bot_or_output_id)
        self._output_low_unresolved = output_low
        self._output_high_unresolved = output_high

        # Outputs which have been resolved to a bot or an output
        self._output_low = None
        self._output_high = None

        # Input that is waiting to be processed
        self._input = []

        # (low, high) values which have been through this bot
        self._compared = []

    def resolve(self):
        self._output_low = self._botnet.get_bot_or_output(
            *self._output_low_unresolved
        )
        self._output_high = self._botnet.get_bot_or_output(
            *self._output_high_unresolved
        )

    def append(self, value):
        self._input.append(value)

        if len(self._input) == 2:
            # Process the inputs now
            self._input.sort()
            value_low, value_high = self._input

            # Record the values I've seen
            self._compared.append((value_low, value_high))

            # Pass them on to my outputs
            self._output_low.append(value_low)
            self._output_high.append(value_high)

    def has_compared(self, value_low, value_high):
        return (value_low, value_high) in self._compared


class BotNet(object):
    def __init__(self, input):
        # bot_id -> Bot instance
        self._bots = {}

        # (bot_id, input)
        self._inputs = []

        # output_id -> queue
        self._outputs = {}

        # Create bots & save input values
        for instruction in input.split('\n'):
            parts = instruction.split(' ')
            if parts[0] == 'value':
                # Input value
                self._inputs.append(
                    (int(parts[5]), int(parts[1]))
                )
            else:
                # A bot definition
                bot_id = int(parts[1])
                output_low = (parts[5], int(parts[6]))
                output_high = (parts[10], int(parts[11]))
                self._bots[bot_id] = Bot(self, bot_id, output_low, output_high)

        # Resolve bot outputs to queues
        for bot in self._bots.values():
            bot.resolve()

        # Put the inputs in
        for bot_id, value in self._inputs:
            self._bots[bot_id].append(value)

    def get_bot_or_output(self, type, bot_or_output_id):
        if type == 'bot':
            return self.get_bot(bot_or_output_id)
        return self.get_output(bot_or_output_id)

    def get_bot(self, bot_id):
        return self._bots[bot_id]

    def get_output(self, output_id):
        if output_id not in self._outputs:
            self._outputs[output_id] = []
        return self._outputs[output_id]

    def output_compared(self):
        for bot_id, bot in self._bots.items():
            print bot_id, '->', bot._compared

    def find_compared(self, value_low, value_high):
        # Find the ID of the bot which compared (value_low, value_high)
        for bot_id, bot in self._bots.items():
            if bot.has_compared(value_low, value_high):
                return bot_id


TEST_INPUT = """value 5 goes to bot 2
bot 2 gives low to bot 1 and high to bot 0
value 3 goes to bot 1
bot 1 gives low to output 1 and high to bot 0
bot 0 gives low to output 2 and high to output 0
value 2 goes to bot 2"""

test_net = BotNet(TEST_INPUT)
# test_net.output_compared()

assert test_net.get_bot(0)._compared == [(3, 5)]
assert test_net.get_bot(1)._compared == [(2, 3)]
assert test_net.get_bot(2)._compared == [(2, 5)]
assert test_net.get_bot(0).has_compared(3, 5) == True
assert test_net.get_bot(0).has_compared(2, 3) == False
assert test_net.find_compared(2, 5) == 2

real_net = BotNet(INPUT)
# real_net.output_compared()
print real_net.find_compared(17, 61)

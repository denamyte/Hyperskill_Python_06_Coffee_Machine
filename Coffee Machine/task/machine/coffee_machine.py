from typing import List, Dict, Callable, Any

buy_action, fill_action, take_action, rem_action, exit_action = \
    'buy', 'fill', 'take', 'remaining', 'exit'
resources = [400, 540, 120, 9, 550]
coffee_costs = [[-250, 0, -16, -1, 4],  # espresso
                [-350, -75, -20, -1, 7],  # latte
                [-200, -100, -12, -1, 6]]  # cappuccino
res_names = ['water', 'milk', 'coffee beans', 'cups']
add_prompts = ['\nWrite how many ml of water do you want to add:\n',
               'Write how many ml of milk do you want to add:\n',
               'Write how many grams of coffee beans do you want to add:\n',
               'Write how many disposable cups of coffee do you want to add:\n']


class Modes:
    select_action = 1
    buy, fill, take, remaining, exit_action = range(2, 7)
    select_buy = 10
    sel_action_dict: Dict[str, int] = {"buy": buy,
                                       "fill": fill,
                                       "take": take,
                                       "remaining": remaining,
                                       "exit": exit_action}


class CoffeeMachine:
    main_action_prompt = 'Write action (buy, fill, take, remaining, exit):'
    buy_prompt = '\nWhat do you want to buy? 1 - espresso, 2 - latte, 3 - cappuccino, back - to main menu:'

    def __init__(self, water: int, milk: int, beans: int, cups: int, money: int):
        self.resources: List[int] = [water, milk, beans, cups, money]
        self.mode: int = Modes.select_action
        self.inputs: Dict[int, Callable[[str], None]] = {Modes.select_action: self.accept_select_action,
                                                         Modes.select_buy: self.accept_select_buy}
        self.actions: Dict[int, Callable[[], None]] = {Modes.remaining: self.show_remaining,
                                                       Modes.buy: self.show_buy}
        self.show_str = CoffeeMachine.main_action_prompt

    def running(self) -> bool:
        return self.mode != Modes.exit_action

    def accept(self, input_str: str):
        self.inputs[self.mode](input_str)

    def accept_select_action(self, select: str):
        self.mode = Modes.sel_action_dict[select]
        self.actions[self.mode]()

    def accept_select_buy(self, select: str):
        if select == 'back':
            self.show_str = f'\n{self.main_action_prompt}'
        else:
            pass
        self.mode = Modes.select_action

        # TODO Finish this method

    def show_remaining(self):
        res = self.resources[:]
        res[-1] = '$' + str(res[-1]) if res[-1] > 0 else 0
        self.show_str = '''\nThe coffee machine has:
{} of water
{} of milk
{} of coffee beans
{} of disposable cups
{} of money

{}'''.format(*res, self.main_action_prompt)
        self.mode = Modes.select_action

    def show_buy(self):
        self.show_str = self.buy_prompt
        self.mode = Modes.select_buy


def main_loop():
    machine = CoffeeMachine(400, 540, 120, 9, 550)
    while machine.running():
        print(machine.show_str)
        machine.accept(input())


main_loop()

# ==================================================================
# ==================================================================
# ==================================================================
# ==================================================================
# FIXME: The code below is old and deprecated

def main():
    action = input_action()
    while action != exit_action:
        actions[action]()
        print()
        action = input_action()


def input_action() -> str:
    return input('Write action (buy, fill, take, remaining, exit):\n')


def buy():
    request = input('\nWhat do you want to buy? 1 - espresso, 2 - latte, 3 - cappuccino, back - to main menu:\n')
    if request == 'back':
        return
    costs = coffee_costs[int(request) - 1]
    scarce_ind = get_scarce_resource_index(costs)
    if scarce_ind >= 0:
        print(f'Sorry, not enough {res_names[scarce_ind]}!')
        return
    print('I have enough resources, making you a coffee!')
    for i in range(5):
        resources[i] += costs[i]


def get_scarce_resource_index(costs: List[int]) -> int:
    """ Returns the index of the first insufficient resource found, -1 otherwise. """
    for i in range(len(res_names)):
        if resources[i] + costs[i] < 0:
            return i
    return -1


def fill():
    for i in range(4):
        resources[i] += int(input(add_prompts[i]))


def take():
    print(f'\nI gave you ${resources[-1]}')
    resources[-1] = 0


def show():
    res = resources[:]
    res[-1] = '$' + str(res[-1]) if res[-1] > 0 else 0
    print('''\nThe coffee machine has:
{} of water
{} of milk
{} of coffee beans
{} of disposable cups
{} of money'''.format(*res))


actions = {buy_action: buy,
           fill_action: fill,
           take_action: take,
           rem_action: show}

# main()

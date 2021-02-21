# This implementation has 1 print() and 1 input() outside of the CoffeeMachine class.

from typing import List, Dict, Callable


class Const:
    start_resources = [400, 540, 120, 9, 550]
    coffee_costs = [[-250, 0, -16, -1, 4],  # espresso
                    [-350, -75, -20, -1, 7],  # latte
                    [-200, -100, -12, -1, 6]]  # cappuccino
    max_fill_index = 3
    main_action_prompt = 'Write action (buy, fill, take, remaining, exit):'
    purchase_prompt = '\nWhat do you want to buy? 1 - espresso, 2 - latte, 3 - cappuccino, back - to main menu:'
    back_request = 'back'
    not_enough_msg = 'Sorry, not enough {}!'
    making_coffee_msg = 'I have enough resources, making you a coffee!'
    res_names = ['water', 'milk', 'coffee beans', 'cups']
    add_prompts = ['\nWrite how many ml of water do you want to add:',
                   'Write how many ml of milk do you want to add:',
                   'Write how many grams of coffee beans do you want to add:',
                   'Write how many disposable cups of coffee do you want to add:']
    remaining_info = '\nThe coffee machine has:'\
                     '\n{} of water\n{} of milk\n{} of coffee beans\n{} of disposable cups\n${} of money\n\n{}'


class Modes:
    # modes to process the query string
    top_level_request, purchase_request, add_resource_request = range(1, 4)
    # modes to show something
    show_menu, show_fill_prompt, show_take, show_remaining, show_exit = range(1, 6)
    top_level_show_actions: Dict[str, int] = {"buy": show_menu,
                                              "fill": show_fill_prompt,
                                              "take": show_take,
                                              "remaining": show_remaining,
                                              "exit": show_exit}


class CoffeeMachine:

    def __init__(self, water: int, milk: int, beans: int, cups: int, money: int):
        self.resources: List[int] = [water, milk, beans, cups, money]
        self.request_mode: int = Modes.top_level_request
        self.show_mode: int = -1
        self.fill_index = 0
        self.show_str = Const.main_action_prompt

        self.request_actions: Dict[int, Callable[[str], None]] = {
            Modes.top_level_request: self.request_top_level_action,
            Modes.purchase_request: self.request_buy_action,
            Modes.add_resource_request: self.request_add_resource,
        }
        self.show_actions: Dict[int, Callable[[], None]] = {
            Modes.show_menu: self.show_menu,
            Modes.show_fill_prompt: self.show_fill_prompt,
            Modes.show_remaining: self.show_remaining,
            Modes.show_take: self.show_take,
            Modes.show_exit: lambda: ...,
        }

    def running(self) -> bool:
        return self.show_mode != Modes.show_exit

    def request_dispatcher(self, request: str):
        self.request_actions[self.request_mode](request)

    def request_top_level_action(self, request: str):
        self.show_mode = Modes.top_level_show_actions[request]
        self.show_actions[self.show_mode]()

    def request_buy_action(self, request: str):
        if request == Const.back_request:
            self.show_str = f'\n{Const.main_action_prompt}'
        else:
            costs = Const.coffee_costs[int(request) - 1]
            scarce_ind = self.get_scarce_resource_index(costs)
            if scarce_ind >= 0:
                self.show_str = self.not_enough_resource_str(scarce_ind)
            else:
                self.show_str = self.making_coffee_str()
                for i in range(len(self.resources)):
                    self.resources[i] += costs[i]
        self.request_mode = Modes.top_level_request

    def get_scarce_resource_index(self, costs: List[int]) -> int:
        for i in range(len(Const.res_names)):
            if self.resources[i] + costs[i] < 0:
                return i
        return -1

    def request_add_resource(self, request: str):
        self.resources[self.fill_index] += int(request)
        self.fill_index += 1
        self.show_fill_prompt()

    def show_menu(self):
        self.show_str = Const.purchase_prompt
        self.request_mode = Modes.purchase_request

    def show_fill_prompt(self):
        if self.fill_index <= Const.max_fill_index:
            self.request_mode = Modes.add_resource_request
            self.show_str = Const.add_prompts[self.fill_index]
        else:
            self.fill_index = 0
            self.request_mode = Modes.top_level_request
            self.show_str = f'\n{Const.main_action_prompt}'

    def show_remaining(self):
        self.show_str = self.remaining_str(self.resources[:])
        self.request_mode = Modes.top_level_request

    def show_take(self):
        self.show_str = self.take_money_str(self.resources[-1])
        self.resources[-1] = 0
        self.request_mode = Modes.top_level_request

    @staticmethod
    def remaining_str(res: List[int]):
        return Const.remaining_info.format(*res, Const.main_action_prompt)

    @staticmethod
    def not_enough_resource_str(scarce_ind: int):
        return CoffeeMachine.purchase_response_str(Const.not_enough_msg.format(Const.res_names[scarce_ind]))

    @staticmethod
    def making_coffee_str():
        return CoffeeMachine.purchase_response_str(Const.making_coffee_msg)

    @staticmethod
    def purchase_response_str(purchase_resume: str):
        return f'''{purchase_resume}\n\n{Const.main_action_prompt}'''

    @staticmethod
    def take_money_str(money: int):
        return f'''\nI gave you ${money}\n\n{Const.main_action_prompt}'''


def main_loop():
    machine = CoffeeMachine(*Const.start_resources)
    while machine.running():
        print(machine.show_str)
        machine.request_dispatcher(input())


main_loop()

from typing import List

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
main()

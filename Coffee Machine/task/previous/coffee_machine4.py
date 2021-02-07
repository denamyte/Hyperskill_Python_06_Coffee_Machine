from typing import List

buy_action, fill_action, take_action = 'buy', 'fill', 'take'
resources = [400, 540, 120, 9, 550]
coffee_costs = [[-250, 0, -16, -1, 4],  # espresso
                [-350, -75, -20, -1, 7],  # latte
                [-200, -100, -12, -1, 6]]  # cappuccino
add_prompts = ['Write how many ml of water do you want to add:\n',
               'Write how many ml of milk do you want to add:\n',
               'Write how many grams of coffee beans do you want to add:\n',
               'Write how many disposable cups of coffee do you want to add:\n']


def main():
    show_resources()
    branches[input_action()]()
    print()
    show_resources()


def show_resources():
    print('''The coffee machine has:
{} of water
{} of milk
{} of coffee beans
{} of disposable cups
{} of money'''.format(*resources))


def input_action() -> str:
    return input('\nWrite action (buy, fill, take):\n')


def buy_branch():
    drink = -1 + int(input('What do you want to buy? 1 - espresso, 2 - latte, 3 - cappuccino:\n'))
    costs = coffee_costs[drink]
    for i in range(5):
        resources[i] += costs[i]


def fill_branch():
    for i in range(4):
        resources[i] += int(input(add_prompts[i]))


def take_branch():
    money, resources[4] = resources[4], 0
    print(f'I gave you ${money}')


branches = {buy_action: buy_branch,
            fill_action: fill_branch,
            take_action: take_branch}
main()

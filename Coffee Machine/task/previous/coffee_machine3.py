from typing import List

prompts = ['Write how many ml of water the coffee machine has:\n',
           'Write how many ml of milk the coffee machine has:\n',
           'Write how many grams of coffee beans the coffee machine has:\n',
           'Write how many cups of coffee you will need:\n']
required = [200, 50, 15]


def main():
    loaded = load()
    can_do_cups = calculate_min_amount(loaded)
    print(report_message(loaded[-1], can_do_cups))


def load() -> List[int]:
    return [int(input(prompt)) for prompt in prompts]


def calculate_min_amount(loaded: List[int]) -> int:
    return min([a // b for a, b in zip(loaded, required)])


def report_message(needed_cups: int, can_do_cups: int):
    if needed_cups <= can_do_cups:
        msg = 'Yes, I can make that amount of coffee'
        if needed_cups < can_do_cups:
            msg += f' (and even {can_do_cups - needed_cups} more than that)'
    else:
        msg = f'No, I can make only {can_do_cups} cups of coffee'
    return msg


main()

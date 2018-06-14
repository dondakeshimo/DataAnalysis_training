import numpy as np
import sys
from tqdm import tqdm


def release_coin(people):
    random = np.random.rand() * 6 + 0.5
    random = np.round(random)

    if random == 1:
        people["person1"] -= 1
    elif random == 2:
        people["person2"] -= 1
    elif random == 3:
        people["person3"] -= 1
    elif random == 4:
        people["person4"] -= 1
    elif random == 5:
        people["person5"] -= 1
    elif random == 6:
        people["person6"] -= 1
    else:
        print("error")
        print(random)

    return people


def get_coin(people):
    random = np.random.rand() * 6 + 0.5
    random = np.round(random)

    if random == 1:
        people["person1"] += 1
    elif random == 2:
        people["person2"] += 1
    elif random == 3:
        people["person3"] += 1
    elif random == 4:
        people["person4"] += 1
    elif random == 5:
        people["person5"] += 1
    elif random == 6:
        people["person6"] += 1
    else:
        print("error")
        print(random)

    return people


def validation(people):
    total = sum(people.values())

    if total == 600:
        return True
    else:
        return False


def main(loop_num):
    people = {"person1": 100,
              "person2": 100,
              "person3": 100,
              "person4": 100,
              "person5": 100,
              "person6": 100}

    for _ in tqdm(range(loop_num)):
        people = release_coin(people)
        people = get_coin(people)
        val = validation(people)

        if val:
            continue
        else:
            print("error")
            print(people)

    print(people)


if __name__ == "__main__":
    arg = int(sys.argv[1])
    main(arg)

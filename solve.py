import equations_solver
import random
import sys


MENU = '''\n\t1: Rozwiaz uklad rownan
        2: Rozwiaz uklady rownan z pliku
        3: Zapisz losowe uklady rownan do pliku
        4: Wyjście z programu'''


def save_data():
    amount = input('Liczba ukladow do wygenerowania: ')
    filename = input('Nazwa pliku: ')
    try:
        generate_random_data(int(amount), filename)
    except ValueError:
        print('\nNiepoprawna liczba')
        return
    print(f'\nPoprawnie wygenerowano i zapisano do pliku {filename}')


def generate_random_data(amount, filename):
    with open(filename, 'w') as data:
        datas = []
        for k in range(amount):
            size = random.randint(2, 3)
            line = f'{size}:'
            for i in range(size):
                for j in range(size + 1):
                    # value = round(random.random() * random.randint(1, 10), 1)
                    value = random.randint(1, 10)
                    line += f'{value};'
                line = f'{line[:-1]}:'
            datas.append(line[:-1])
        data.write('\n'.join(datas) + '\n')


def _exit():
    """Wychodzi z programu."""
    sys.exit()


def handle_solve_linear_system():
    size, left_, right_ = ask_for_data()
    solve(size, left_, right_)



def solve(size, left_, right_):
    p = equations_solver.Solver()
    p.solve(size, left_, right_)
    values = str(p)[:-1].split(':')
    if(len(values) <= 1):
        print('UKLAD SPRZECZNY')
        print()
        return
    for index, value in enumerate(values):
        print(f'x_{index}: {value}')
    print()


def ask_for_data():
    size = input('Podaj liczbe niewiadomych: ')
    all_info, info = '', ''
    left_, right_ = [], []
    for i in range(int(size)):
        print()
        single_left_ = []
        for i in range(int(size) + 1):
            if(i == int(size)):
                value = input('prawa strona = ')
                right_.append(float(value))
                info = info[:-2] + f' = {value}'
            else:
                value = input(f'wspolczynnik x_{i} = ')
                single_left_.append(float(value))
                info += f'{value} * x_{i} + '
        left_.append(single_left_)
        all_info += f'{info}\n'
        info = ''
    print(f'\n{all_info}')
    input('\nOblicz').split(" ")[0]
    return int(size), left_, right_


def handle_solve_systems_from_file():
    filename = input('Podaj nazwe pliku: ')
    solve_systems_from_file(filename)


def solve_systems_from_file(filename):
    err_line_ = '=' * 70
    try:
        with open(filename) as data:
            linear_systems = data.readlines()
            for line_counter, linear_system in enumerate(linear_systems, start=1):
                left_, right_ = [], []
                correct_format = True
                lines = linear_system.strip().split(':')
                try:
                    size = int(lines[0])
                except ValueError as e:
                    print(
                            f'{err_line_}\n ERROR : Niewlasciwie sformatowana {line_counter}'
                            f' linia!\n = Niepoprawny rozmiar - {str(e)}\n{err_line_}')
                    continue
                for line in lines[1:]:
                    values = line.split(';')
                    try:
                        if(len(values) != size + 1):
                            print(
                                    f'{err_line_}\n ERROR : Niewlasciwie sformatowana {line_counter} linia!'
                                    f'\n = Nie zgadza sie liczba wewnetrznych wartosci\n{err_line_}')
                            correct_format = False
                            break
                        left_.append([float(i) for i in values[:-1]])
                        right_.append(float(values[-1]))
                    except ValueError as e:
                        print(
                                f'{err_line_}\n ERROR : Niewlasciwie sformatowana {line_counter} linia!'
                                f'\n = Niepoprawne wartosci - {str(e)}\n{err_line_}')
                        correct_format = False
                        break
                if(not correct_format):
                    continue
                if(len(left_) != size or len(right_) != size):
                    print(
                            f'{err_line_}\n ERROR : Niewlasciwie sformatowana {line_counter} linia!'
                            f'\n = Nie zgadza sie liczba wartosci\n{err_line_}')
                    continue
                print()
                print(f'Rownanie nr {line_counter} ({linear_system.strip()}):')
                solve(size, left_, right_)
    except FileNotFoundError as f:
        print(f'\nBlad przy otwieraniu pliku - {str(f)}')


SWITCHER = {
    '1': handle_solve_linear_system,
    '2': handle_solve_systems_from_file,
    '3': save_data,
    '4': _exit
}


def menu():
    ans = 0
    while(ans != 4):
        print(MENU)
        ans = input("\nCo chcesz zrobic?: ")
        SWITCHER[ans]()


if __name__ == "__main__":
    menu()

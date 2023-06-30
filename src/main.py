# -*- coding: utf-8 -*-


import psutil
from args_parser import parser


# Global settings
settings = parser.parse_args()


def configure_settings():
    """
    Configure settings: split agrs on ',' (make lists), Fixing
    """
    settings.user_names = settings.user_names.split(',')
    settings.ps_names = settings.ps_names.split(',')
    settings.exclude_user_names = settings.exclude_user_names.split(',')

    if settings.mode not in ['kill', 'show']:
        settings.mode = 'show'


def get_ps_list() -> list:
    ps_iter = psutil.process_iter(['pid', 'name', 'username'])
    return [ps for ps in ps_iter]


def filter_ps_list(ps_list: list,
                   ps_names: list,
                   user_names: list,
                   exclude_user_names: list):

    def filter_ps_names(ps_list: list, ps_names: list) -> list:
        return filter(lambda ps: ps.info['name'] in ps_names,
                      ps_list)

    def filter_user_names(ps_list: list, user_names: list) -> list:

        def ps_user_in_users(ps) -> bool:
            try:
                if ps.username().split('\\')[1] in user_names:
                    return True
            except IndexError:
                if ps.username() in user_names:
                    return True
            return False

        return filter(ps_user_in_users, ps_list)

    def filter_exclude_user_names(ps_list: list,
                                  exclude_user_names: list
                                  ) -> list:

        def ps_user_not_in_exclude_users(ps) -> bool:
            try:
                if ps.username().split('\\')[1] in exclude_user_names:
                    return False
            except IndexError:
                if ps.username() in exclude_user_names:
                    return False
            return True

        return filter(ps_user_not_in_exclude_users, ps_list)

    # отфильтровать по имени процессов
    if ps_names[0]:
        ps_list = filter_ps_names(ps_list, ps_names)

    # отфильтровать по именам пользователей
    if user_names[0]:
        ps_list = filter_user_names(ps_list, user_names)

    # отфильтровать по именам пользователей для исклчения
    if exclude_user_names[0]:
        ps_list = filter_exclude_user_names(ps_list, exclude_user_names)

    # вернуть отфильтрованный список
    return ps_list


def print_ps_data(ps, mode):
        message = ''

        try:
            message += f'{ps.username()} '
        except psutil.AccessDenied:
            pass

        if mode == 'kill':
            message += f'KILLING '

        try:
            message += f'[pid {ps.info["pid"]}] '
        except psutil.AccessDenied:
            pass

        try:
            message += f'{ps.info["name"]} '
        except psutil.AccessDenied:
            pass

        try:
            message += f'({ps.exe()}), '
        except psutil.AccessDenied:
            pass

        message += f'RAM: {ps.memory_percent()}%'

        print(message)


def go(ps_list: list, mode: str):
    ram_percent_count = 0  # init

    for ps in ps_list:
        ram_percent_count += ps.memory_percent()

        print_ps_data(ps, mode)

        if mode == 'kill':
            try:
                ps.terminate()
            except:
                print('ACCESS DENIED')

    if ram_percent_count:
        print(f'Total RAM usage: {ram_percent_count}%.')


def main():

    configure_settings()

    ps_list = get_ps_list()
    ps_list = filter_ps_list(ps_list,
                             settings.ps_names,
                             settings.user_names,
                             settings.exclude_user_names,
                             )

    go(ps_list, settings.mode)


if __name__ == '__main__':
    main()


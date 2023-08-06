from lib.lib import *
import sys


def login_flow(email, password):
    # TODO Try to login
    # email = input("Please enter your email: ")
    # password = input("Please enter your password: ")
    email = "bgomes@youongroup.com"
    password = "1234567"

    key = cookie_id(email, password)

    r = login(email, password)
    print(r)

    ## TODO Test if success of r
    accounts = list_accounts(r)
    print(accounts)

    ## token = "5nff7dqpce5u4moq"  ## Local
    token = "debug-6cb92e4a4e74e90a29f206b4ecd8c5fd" ## Production
    r = choose_account(r, token)

    # requestsCookieJar = r.cookies

    # Update the cookie
    update_cookie(key, r.cookies)


def main():
    email = "bgomes@youongroup.com"
    password = "1234567"
    is_logged_in = False

    # email = input("Please enter your email: ")
    # password = input("Please enter your password: ")

    key = cookie_id(email, password)

    requestsCookieJar = load_cookie(key)
    if isinstance(requestsCookieJar, requests.cookies.RequestsCookieJar):
        is_expired = cookie_is_expired(requestsCookieJar)

        # If cookie is not expired than update cookie
        if not is_expired:
            print("Loading previsious login")
            update_cookie(key, requestsCookieJar)
        else:
            while is_expired:
                # TODO Show login prompt
                print("Show login form")

                login_flow("", "")

    else:
        print("Not instance, than show loggin form")
        login_flow("", "")

    # r1 = login("bgomes@youongroup.com", "1234567")
    # print(r1)
    # expires = next(x for x in r1.cookies if x.name == 'sts').expires
    # is_expired = next(x for x in r1.cookies if x.name == 'sts').is_expired()
    # print(is_expired)

    # accounts = listAccounts(login(email, password))
    # print(accounts)

    # token = "5nff7dqpce5u4moq"
    # r2 = chooseAccount(r1, token)

    # Get videos
    # print(s.cookies)
    r = get_videos()
    # print(r.text)

    # r = get_videos()
    # print(r.text)

    # Start uploading
    start()
    # Start with an empty list. You can 'seed' the list with
    # some predefined values if you like.
    names = []

    # Set new_name to something other than 'quit'.
    new_name = 'quit'

    while new_name != 'quit':
        # Ask the user for a name.
        new_name = input("Please tell me someone I should know, or enter 'quit': ")

        # Add the new name to our list.
        if new_name != 'quit':
            names.append(new_name)

    # Show that the name has been added to the list.
    # print(names)


if __name__ == "__main__":
    main()

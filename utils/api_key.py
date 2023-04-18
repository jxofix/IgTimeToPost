# store and retrieve Instagram Access Token
import keyring


# create keyring entry
def create_entry(namespace: str, entry: str, password: str) -> bool:
    """
    Function to store credentials to keyring
    :param namespace: keyring namespace
    :param entry: naming stored password
    :param password: password to be stored
    :return: True if credentials were saved correctly
    """
    keyring.set_password(namespace, entry, password)
    creds = keyring.get_credential(namespace, entry)

    return creds.password == password


# get keyring password/api
def get_entry(entry: str, namespace: str = 'time_to_post') -> str:
    """
    Function to receive credentials from keyring
    :param entry: naming stored password
    :param namespace: keyring namespace
    :return: credentials for required namespace and entry
    """
    creds = keyring.get_credential(namespace, entry)

    return creds.password


# save new passwords
# if __name__ == '__main__':
#     NAMESPACE = ''
#     ENTRY = ''
#     PASSWORD = ''
#     print(create_entry(NAMESPACE, ENTRY, PASSWORD))




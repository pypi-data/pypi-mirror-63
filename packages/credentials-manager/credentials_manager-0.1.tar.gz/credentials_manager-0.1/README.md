CredentialsManager
==================

Simple python credentials manager which uses home directory files and the keyring module.

Usage example:

    cm = CredentialsManager()
    cm.load()
    login_to_external_service(username=cm.username, password=cm.password)

from kuisioner import kuisioner


if __name__ == "__main__":
    username = "Username"
    password = "Password"
    kuisioner = kuisioner(username, password)
    kuisioner.login()
    kuisioner.kuis()

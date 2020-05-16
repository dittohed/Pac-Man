try:
    raise NameError("Hi there")  # rzuć wyjątek
except NameError:
    print("An exception")

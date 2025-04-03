import re


def validate_document(document: str) -> bool:
    value = re.sub(r"[()./-]", "", document)
    value = re.sub(r"[\s]", "", value)

    if not re.match(
        r"^([0-9]{11})$|^([0-9]{14})$",
        value,
    ):
        return False
    else:
        if len(value) == 11:
            if value == value[0] * len(value):
                return False
            else:
                for i in range(9, 11):
                    soma = sum(int(value[j]) * (i + 1 - j) for j in range(i))
                    digito = (soma * 10 % 11) % 10
                    if digito != int(value[i]):
                        return False
        elif len(value) == 14:
            if value == value[0] * len(value):
                return False
            else:
                pesos_1 = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
                pesos_2 = [6] + pesos_1

                for i in range(12, 14):
                    soma = (
                        sum(int(value[j]) * pesos_1[j] for j in range(i))
                        if i == 12
                        else sum(int(value[j]) * pesos_2[j] for j in range(i))
                    )
                    digito = soma % 11
                    digito = 0 if digito < 2 else 11 - digito
                    if digito != int(value[i]):
                        return False

    return True

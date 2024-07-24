import re 

def validate_card(card_number):
    card_final: list[int] = str_to_int(card_number)
    if luhn_algo(card_final):
        return True, card_type(card_number)
    else:
        return False, ""
    
def luhn_algo(card_number) -> bool:
    odd_digits: list[int] = card_number[-1::-2]  
    even_digits: list[int] = card_number[-2::-2]
    totalSum: int = sum(odd_digits)
    print(totalSum)
    for dig in even_digits:
        value: int = dig * 2
        if value >= 10:
            new = value - 9
            print(new)
            totalSum += new
            print(totalSum)
        else:
            totalSum += value
    print("Sum:" + str(totalSum) + "\n")
    return totalSum % 10 == 0 

def str_to_int(card_string):
    return [int(s) for s in str(card_string)]

def card_type(card_number) -> str:
    potential_types = {
        "Visa": r"^4[0-9]{12}(?:[0-9]{3})?$",  
        "MasterCard": r"^5[1-5][0-9]{14}$",  
        "American Express": r"^3[47][0-9]{13}$", 
        "Discover": r"^6(?:011|5[0-9]{2})[0-9]{12}$", 
        "JCB": r"^(?:2131|1800|35\d{3})\d{11}$",
        "Diners Club": r"^3(?:0[0-5]|[68][0-9])[0-9]{11}$", 
        "Maestro": r"^(5018|5020|5038|56|57|58|6304|6759|676[1-3])\d{8,15}$", 
        "Verve": r"^(506[01]|507[89]|6500)\d{12,15}$" 
    }
    for card_type, pattern in potential_types.items():
        if re.match(pattern, card_number):  # Check if card number matches the pattern
            return card_type
    return "Unknown"  
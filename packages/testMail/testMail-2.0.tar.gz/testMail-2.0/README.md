# testMail

## How to install
```
git clone https://github.com/FKgk/testMail.git
```
or
```
pip install testMail
```

## Dependency
- this package don't need any reqiurements
- need built-in module (email, smtplib, re)

## Example
```
from testMail import Mail

mail = Mail("sender email", "app password")

# support one string and list
mail.send("receiver email", "title", "content")

mail.close()
```

### If you want to check validation
```
mail.valid("email")
```
- return true or raise WrongEmailError

## Reference
- [smtp](https://docs.python.org/3/library/smtplib.html)
- [google app password](https://support.google.com/accounts/answer/185833?hl=ko)

## PYPI
- https://pypi.org/project/testMail/1.3/
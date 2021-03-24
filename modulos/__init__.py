DOMINIO_CORREO_ISTA = '@tecazuay.edu.ec'

def validar_email(correo: str) -> bool:

    if len(correo) >= 17 and len(correo) < 75 and correo.endswith(DOMINIO_CORREO_ISTA) and correo.count('@') == 1:

        try:
            start_email = correo.split('@')[0]

            if start_email.replace('.','').isalpha():
                return True
            else:
                return False

        except Exception:
            return False
            print ('asd')

    else:
        return False

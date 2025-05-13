"""Internationalization module."""
from typing import Dict, Any

# English messages
en_messages = {
    "auth": {
        "invalid_credentials": "Incorrect email or password",
        "user_not_found": "User not found",
        "email_exists": "Email already registered",
        "weak_password": "Password must be at least 8 characters long and contain at least one uppercase letter, one lowercase letter, one number and one special character",
        "password_recovery_sent": "Password recovery email sent",
        "password_updated": "Password updated successfully",
        "invalid_token": "Invalid or expired token",
        "too_many_requests": "Too many requests. Please try again later.",
        "inactive_user": "This account is inactive",
        "email_send_error": "Error sending password recovery email. Please try again later.",
        "password_recovery_error": "An error occurred during password recovery. Please try again later.",
    }
}

# Portuguese messages
pt_br_messages = {
    "auth": {
        "invalid_credentials": "Email ou senha incorretos",
        "user_not_found": "Usuário não encontrado",
        "email_exists": "Email já cadastrado",
        "weak_password": "A senha deve ter pelo menos 8 caracteres e conter pelo menos uma letra maiúscula, uma letra minúscula, um número e um caractere especial",
        "password_recovery_sent": "Email de recuperação de senha enviado",
        "password_updated": "Senha atualizada com sucesso",
        "invalid_token": "Token inválido ou expirado",
        "too_many_requests": "Muitas requisições. Por favor, tente novamente mais tarde.",
        "inactive_user": "Esta conta está inativa",
        "email_send_error": "Erro ao enviar email de recuperação de senha. Por favor, tente novamente mais tarde.",
        "password_recovery_error": "Ocorreu um erro durante a recuperação de senha. Por favor, tente novamente mais tarde.",
    }
}

# Message dictionary
messages: Dict[str, Dict[str, Any]] = {
    "en": en_messages,
    "pt-br": pt_br_messages,
}


def get_message(language: str, key: str, *path: str) -> str:
    """Get a message in the specified language."""
    # Default to English if language not supported
    if language not in messages:
        language = "en"

    # Navigate through the message dictionary
    current = messages[language]
    for p in path:
        if p not in current:
            # Fall back to English if key not found
            current = messages["en"]
            for p2 in path:
                current = current.get(p2, {})
        else:
            current = current[p]

    # If key not found, return key itself
    return current.get(key, key)

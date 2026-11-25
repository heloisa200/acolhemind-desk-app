import hashlib
import hmac
import secrets

from database.connection import conectar

ITERACOES = 200_000  # custo do PBKDF2: deixa ataques de força bruta lentos
TAMANHO_MIN_SENHA = 8


def _gerar_hash(senha: str, salt: bytes) -> str:
    return hashlib.pbkdf2_hmac(
        "sha256", senha.encode("utf-8"), salt, ITERACOES
    ).hex()


def existe_admin() -> bool:
    conn = conectar()
    total = conn.execute("SELECT COUNT(*) FROM usuarios").fetchone()[0]
    conn.close()
    return total > 0


def validar_senha_nova(senha: str):
    """Retorna uma mensagem de erro, ou None se a senha é aceitável."""
    if len(senha) < TAMANHO_MIN_SENHA:
        return f"A senha precisa ter pelo menos {TAMANHO_MIN_SENHA} caracteres."
    if senha.isalpha() or senha.isdigit():
        return "Misture letras e números na senha."
    return None


def criar_admin(usuario: str, senha: str) -> None:
    """Cria o administrador. Só funciona se ainda não existir nenhum."""
    if existe_admin():
        raise PermissionError("Já existe um administrador cadastrado.")

    salt = secrets.token_bytes(16)
    conn = conectar()
    conn.execute(
        "INSERT INTO usuarios (usuario, senha_hash, salt) VALUES (?, ?, ?)",
        (usuario, _gerar_hash(senha, salt), salt.hex()),
    )
    conn.commit()
    conn.close()


def autenticar(usuario: str, senha: str) -> bool:
    conn = conectar()
    linha = conn.execute(
        "SELECT senha_hash, salt FROM usuarios WHERE usuario = ?", (usuario,)
    ).fetchone()
    conn.close()

    if linha is None:
        # Faz o mesmo trabalho de hash para não revelar se o usuário existe
        _gerar_hash(senha, b"0" * 16)
        return False

    senha_hash, salt_hex = linha
    calculado = _gerar_hash(senha, bytes.fromhex(salt_hex))
    return hmac.compare_digest(calculado, senha_hash)


def alterar_senha(usuario: str, senha_atual: str, senha_nova: str) -> bool:
    if not autenticar(usuario, senha_atual):
        return False

    salt = secrets.token_bytes(16)
    conn = conectar()
    conn.execute(
        "UPDATE usuarios SET senha_hash = ?, salt = ? WHERE usuario = ?",
        (_gerar_hash(senha_nova, salt), salt.hex(), usuario),
    )
    conn.commit()
    conn.close()
    return True

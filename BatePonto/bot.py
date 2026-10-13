
"""
Bot de ponto para Discord.

Comandos:
  /entrar     -> registra a entrada
  /sair       -> registra a saída e mostra o tempo trabalhado
  /status     -> mostra se você está com o ponto aberto
  /relatorio  -> total de horas no mês (você ou outro membro)

Requisitos:
  pip install discord.py
  Defina a variável de ambiente DISCORD_TOKEN com o token do bot.
"""

import os
import sqlite3
from datetime import datetime, timezone
from zoneinfo import ZoneInfo

import discord
from discord import app_commands

DB_PATH = "ponto.db"
TZ = ZoneInfo("America/Sao_Paulo")


# ---------- Banco de dados ----------
def conectar():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def iniciar_db():
    with conectar() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS pontos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                entrada TEXT NOT NULL,
                saida TEXT
            )
            """
        )


def agora_utc():
    return datetime.now(timezone.utc)


def ponto_aberto(conn, user_id):
    return conn.execute(
        "SELECT * FROM pontos WHERE user_id = ? AND saida IS NULL", (user_id,)
    ).fetchone()


def formatar_duracao(segundos):
    segundos = int(segundos)
    h, resto = divmod(segundos, 3600)
    m, s = divmod(resto, 60)
    return f"{h}h {m:02d}min {s:02d}s"


def formatar_hora(dt_utc):
    return dt_utc.astimezone(TZ).strftime("%d/%m/%Y às %H:%M")


# ---------- Bot ----------
class BotPonto(discord.Client):
    def __init__(self):
        super().__init__(intents=discord.Intents.default())
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        iniciar_db()
        await self.tree.sync()


bot = BotPonto()


@bot.event
async def on_ready():
    print(f"Bot conectado como {bot.user}")


@bot.tree.command(name="entrar", description="Bater ponto de entrada")
async def entrar(interaction: discord.Interaction):
    with conectar() as conn:
        if ponto_aberto(conn, interaction.user.id):
            await interaction.response.send_message(
                "Você já tem um ponto aberto. Use /sair antes de entrar de novo.",
                ephemeral=True,
            )
            return
        agora = agora_utc()
        conn.execute(
            "INSERT INTO pontos (user_id, entrada) VALUES (?, ?)",
            (interaction.user.id, agora.isoformat()),
        )
    await interaction.response.send_message(
        f"✅ {interaction.user.mention} entrou em {formatar_hora(agora)}."
    )


@bot.tree.command(name="sair", description="Bater ponto de saída")
async def sair(interaction: discord.Interaction):
    with conectar() as conn:
        aberto = ponto_aberto(conn, interaction.user.id)
        if not aberto:
            await interaction.response.send_message(
                "Você não tem ponto aberto. Use /entrar primeiro.", ephemeral=True
            )
            return
        agora = agora_utc()
        entrada = datetime.fromisoformat(aberto["entrada"])
        conn.execute(
            "UPDATE pontos SET saida = ? WHERE id = ?",
            (agora.isoformat(), aberto["id"]),
        )
    duracao = formatar_duracao((agora - entrada).total_seconds())
    await interaction.response.send_message(
        f"🛑 {interaction.user.mention} saiu em {formatar_hora(agora)}.\n"
        f"Tempo trabalhado: **{duracao}**"
    )


@bot.tree.command(name="status", description="Ver se seu ponto está aberto")
async def status(interaction: discord.Interaction):
    with conectar() as conn:
        aberto = ponto_aberto(conn, interaction.user.id)
    if not aberto:
        await interaction.response.send_message(
            "Você está com o ponto fechado.", ephemeral=True
        )
        return
    entrada = datetime.fromisoformat(aberto["entrada"])
    decorrido = formatar_duracao((agora_utc() - entrada).total_seconds())
    await interaction.response.send_message(
        f"Ponto aberto desde {formatar_hora(entrada)} ({decorrido}).",
        ephemeral=True,
    )


@bot.tree.command(name="relatorio", description="Horas trabalhadas no mês atual")
@app_commands.describe(membro="Membro para consultar (padrão: você)")
async def relatorio(interaction: discord.Interaction, membro: discord.Member = None):
    alvo = membro or interaction.user
    agora = agora_utc()
    inicio_mes = (
        agora.astimezone(TZ)
        .replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        .astimezone(timezone.utc)
    )

    total = 0
    with conectar() as conn:
        linhas = conn.execute(
            "SELECT entrada, saida FROM pontos WHERE user_id = ? AND entrada >= ?",
            (alvo.id, inicio_mes.isoformat()),
        ).fetchall()

    for linha in linhas:
        entrada = datetime.fromisoformat(linha["entrada"])
        saida = datetime.fromisoformat(linha["saida"]) if linha["saida"] else agora
        total += (saida - entrada).total_seconds()

    await interaction.response.send_message(
        f"📊 {alvo.display_name} trabalhou **{formatar_duracao(total)}** "
        f"neste mês ({len(linhas)} registros).",
        ephemeral=True,
    )



if __name__ == "__main__":
    token = os.environ.get("TokenBot")

    if not token:
        raise SystemExit("Defina a variável de ambiente DISCORD_TOKEN.")

    bot.run(token)

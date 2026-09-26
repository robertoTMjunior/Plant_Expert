"""
PlantExpert - Sistema Especialista para Diagnóstico Inicial de Plantas
========================================================================

Implementação baseada no trabalho acadêmico "PlantExpert" (UVA -
Análise Orientada a Objetos, 2026), de Lucas Gonçalves Carvalho Machado.

O programa usa encadeamento para frente (forward chaining):
    1. Coleta fatos (respostas do usuário) sobre sintomas e condições
       de cultivo da planta.
    2. Compara os fatos com a base de conhecimento (regras SE/ENTÃO).
    3. Apresenta a(s) hipótese(s) de diagnóstico e a recomendação
       correspondente, ou informa que nenhuma regra foi satisfeita.

Regras da base de conhecimento (conforme Quadro 1 do trabalho):

    R01: folhas_amareladas E solo_muito_umido E rega_frequente
         -> Possível excesso de água
    R02: folhas_secas E solo_seco E NÃO rega_frequente
         -> Possível falta de água
    R03: folhas_amareladas E pouca_luz
         -> Possível deficiência de luminosidade
    R04: manchas E umidade_alta
         -> Possível problema fúngico
    R05: pequenos_insetos E folhas_danificadas
         -> Possível presença de pragas
"""

from dataclasses import dataclass, field
from typing import Callable, Dict, List


@dataclass
class Regra:
    """Representa uma regra de produção SE/ENTÃO da base de conhecimento."""
    id: str
    descricao_condicao: str
    diagnostico: str
    recomendacoes: List[str]
    condicao: Callable[[Dict[str, bool]], bool]

    def avaliar(self, fatos: Dict[str, bool]) -> bool:
        """Verifica se todas as condições da regra são satisfeitas pelos fatos."""
        return self.condicao(fatos)


class BaseConhecimento:
    """Agrupa as regras de produção do PlantExpert."""

    def __init__(self):
        self.regras: List[Regra] = [
            Regra(
                id="R01",
                descricao_condicao=(
                    "folhas amareladas + solo muito úmido + rega frequente"
                ),
                diagnostico="Possível excesso de água",
                recomendacoes=[
                    "Reduzir a frequência de rega.",
                    "Verificar a drenagem do vaso.",
                    "Observar a evolução por alguns dias.",
                ],
                condicao=lambda f: (
                    f.get("folhas_amareladas", False)
                    and f.get("solo_muito_umido", False)
                    and f.get("rega_frequente", False)
                ),
            ),
            Regra(
                id="R02",
                descricao_condicao=(
                    "folhas secas + solo seco + rega não frequente"
                ),
                diagnostico="Possível falta de água",
                recomendacoes=[
                    "Aumentar gradualmente a rega.",
                    "Verificar a umidade do solo antes de regar novamente.",
                ],
                condicao=lambda f: (
                    f.get("folhas_secas", False)
                    and f.get("solo_seco", False)
                    and not f.get("rega_frequente", False)
                ),
            ),
            Regra(
                id="R03",
                descricao_condicao="folhas amareladas + pouca luz",
                diagnostico="Possível deficiência de luminosidade",
                recomendacoes=[
                    "Avaliar local com iluminação adequada.",
                    "Evitar ambientes muito escuros por longos períodos.",
                ],
                condicao=lambda f: (
                    f.get("folhas_amareladas", False)
                    and f.get("pouca_luz", False)
                ),
            ),
            Regra(
                id="R04",
                descricao_condicao="manchas nas folhas + umidade alta",
                diagnostico="Possível problema fúngico",
                recomendacoes=[
                    "Melhorar a ventilação do ambiente.",
                    "Evitar molhar as folhas ao regar.",
                ],
                condicao=lambda f: (
                    f.get("manchas", False) and f.get("umidade_alta", False)
                ),
            ),
            Regra(
                id="R05",
                descricao_condicao="pequenos insetos + folhas danificadas",
                diagnostico="Possível presença de pragas",
                recomendacoes=[
                    "Inspecionar a planta cuidadosamente.",
                    "Avaliar métodos de controle adequado (ex.: sabão inseticida).",
                ],
                condicao=lambda f: (
                    f.get("pequenos_insetos", False)
                    and f.get("folhas_danificadas", False)
                ),
            ),
        ]


class MotorInferencia:
    """Compara os fatos informados com as regras da base de conhecimento."""

    def __init__(self, base: BaseConhecimento):
        self.base = base

    def diagnosticar(self, fatos: Dict[str, bool]) -> List[Regra]:
        """Retorna a lista de regras cujas condições foram satisfeitas."""
        return [r for r in self.base.regras if r.avaliar(fatos)]


class Historico:
    """Registra os diagnósticos realizados durante a sessão (Registrado no fluxograma)."""

    def __init__(self):
        self.registros: List[Dict] = []

    def registrar(self, fatos: Dict[str, bool], regras_ativadas: List[Regra]):
        self.registros.append(
            {
                "fatos": dict(fatos),
                "diagnosticos": [r.diagnostico for r in regras_ativadas],
            }
        )

    def exibir(self):
        if not self.registros:
            print("\nNenhum diagnóstico registrado nesta sessão.")
            return
        print("\n=== Histórico de diagnósticos ===")
        for i, reg in enumerate(self.registros, start=1):
            print(f"\nConsulta {i}:")
            if reg["diagnosticos"]:
                for d in reg["diagnosticos"]:
                    print(f"  - {d}")
            else:
                print("  - Nenhuma hipótese suficiente foi encontrada.")


def perguntar_sim_nao(pergunta: str) -> bool:
    """Coleta uma resposta SIM/NÃO do usuário e converte para booleano."""
    while True:
        resposta = input(f"{pergunta} (sim/não): ").strip().lower()
        if resposta in ("sim", "s"):
            return True
        if resposta in ("não", "nao", "n"):
            return False
        print("Resposta inválida. Digite 'sim' ou 'não'.")


def coletar_fatos() -> Dict[str, bool]:
    """Implementa a etapa 'Coletar dados e sintomas' do fluxograma."""
    print("\n--- Questionário: sintomas e condições de cultivo ---")
    fatos = {
        "folhas_amareladas": perguntar_sim_nao("Há folhas amareladas?"),
        "folhas_secas": perguntar_sim_nao("Há folhas secas?"),
        "solo_muito_umido": perguntar_sim_nao("O solo permanece muito úmido?"),
        "solo_seco": perguntar_sim_nao("O solo está seco?"),
        "rega_frequente": perguntar_sim_nao("A rega é frequente?"),
        "pouca_luz": perguntar_sim_nao("A planta recebe pouca luz?"),
        "umidade_alta": perguntar_sim_nao("A umidade ambiente está alta?"),
        "manchas": perguntar_sim_nao("Há manchas nas folhas?"),
        "pequenos_insetos": perguntar_sim_nao("Há pequenos insetos na planta?"),
        "folhas_danificadas": perguntar_sim_nao(
            "Há danos ou perfurações nas folhas?"
        ),
    }
    return fatos


def apresentar_resultado(regras_ativadas: List[Regra]):
    """Implementa a etapa 'Apresentar diagnóstico e recomendação' do fluxograma."""
    if not regras_ativadas:
        print("\n=== Resultado ===")
        print("Não foi encontrada uma hipótese suficiente com os dados informados.")
        print("Recomenda-se buscar avaliação especializada.")
        return

    print("\n=== Resultado ===")
    for regra in regras_ativadas:
        print(f"\n{regra.diagnostico}  (regra {regra.id})")
        print("Recomendação:")
        for rec in regra.recomendacoes:
            print(f"  - {rec}")


def menu():
    base = BaseConhecimento()
    motor = MotorInferencia(base)
    historico = Historico()

    print("=" * 50)
    print("PlantExpert - Diagnóstico inicial de plantas")
    print("=" * 50)

    while True:
        print("\n1. Iniciar diagnóstico")
        print("2. Consultar histórico")
        print("3. Sair")
        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            fatos = coletar_fatos()
            regras_ativadas = motor.diagnosticar(fatos)
            apresentar_resultado(regras_ativadas)
            historico.registrar(fatos, regras_ativadas)
        elif opcao == "2":
            historico.exibir()
        elif opcao == "3":
            print("Encerrando o PlantExpert. Até a próxima!")
            break
        else:
            print("Opção inválida. Tente novamente.")


if __name__ == "__main__":
    menu()

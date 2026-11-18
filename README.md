# AcolheMind — Assistente Pré-Consulta (Desk App I)

Software desktop de suporte pré-consulta para pacientes neurodivergentes, desenvolvido em Python (Tkinter) aplicando os conceitos de Programação Orientada a Objetos.

## Diagrama de Classes (UML)

```mermaid
classDiagram
    class EntradaRelato {
        <<abstract>>
        +String conteudo
        +extrair_sintomas()* String
    }
    class RelatoTexto {
        +extrair_sintomas() String
    }
    class RelatoAudio {
        +int duracao_segundos
        +extrair_sintomas() String
    }
    class BaseConhecimento {
        +List~String~ manuais
        +consultar_diretrizes() String
    }
    class ModeradorClinico {
        +validar_seguranca(texto: String) bool
    }
    class Paciente {
        +String nome
        +String id_perfil
        +String neuroatipicidade
        +exibir_perfil() String
    }
    class RelatorioClinico {
        +String motivo_consulta
        +List~String~ sintomas_principais
        +List~String~ gatilhos_sobrecarga
        +adicionar_dados(sintoma: String, gatilho: String)
        +gerar_texto_resumo(paciente, validacao_rag) String
    }
    class SistemaAcolheMind {
        +BaseConhecimento base_conhecimento
        +Dict~String, Paciente~ pacientes_cadastrados
        +RelatorioClinico sessao_relatorio
        +cadastrar_paciente(nome, id_perfil, neuroatipicidade)
        +iniciar_sessao_consulta(motivo_consulta)
        +processar_interacao(entrada, moderador, gatilho)
    }

    EntradaRelato <|-- RelatoTexto : Herança
    EntradaRelato <|-- RelatoAudio : Herança
    SistemaAcolheMind o-- BaseConhecimento : Associação (Agregação)
    SistemaAcolheMind *-- RelatorioClinico : Composição
    SistemaAcolheMind "1" --> "*" Paciente : Associação
    SistemaAcolheMind ..> ModeradorClinico : Dependência
    SistemaAcolheMind ..> EntradaRelato : Dependência
```

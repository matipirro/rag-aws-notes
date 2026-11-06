import argparse
import sys

from src.generator import answer


def main():
    # La consola de Windows (cp1252) no puede imprimir los emojis de los títulos
    sys.stdout.reconfigure(encoding="utf-8")

    parser = argparse.ArgumentParser(description="Pregunta a tus apuntes de AWS")
    parser.add_argument("query")
    parser.add_argument("-k", type=int, default=4, help="chunks de contexto")
    args = parser.parse_args()

    result = answer(args.query, args.k)
    print(result["answer"])
    print("\nFuentes:")
    for source in result["sources"]:
        print(f"  - {source}")


if __name__ == "__main__":
    main()

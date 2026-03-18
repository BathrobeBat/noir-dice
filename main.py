from noir.mechanics import difficulty

def main():
    value = int(input("Ange värde: "))
    r, total, success = difficulty(value)

    print("\n🎲 Resultat")
    print(f"Slag: {r['grundslag']} + {r['extra']}")
    print(f"Summa: {total}")

    if success:
        print("✅ Lyckat!")
    else:
        print("❌ Misslyckat!")

if __name__ == "__main__":
    main()
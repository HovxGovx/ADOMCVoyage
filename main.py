from ga.algo import run
from data.affichage import afficher_individu
def main():
    results = run()
    for i in range(3):
        print(f"\nMeilleur individu {i+1} :")
        afficher_individu(results[i])
if __name__ == "__main__":
    main()
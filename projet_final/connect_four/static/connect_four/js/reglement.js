let liste_reglements = [
    "Connect-Four est un jeu à deux joueurs ressemblant à un tic-tac-toe dans lequel les joueurs placent les dames en alternance sur un tableau vertical. ",
    "Le tableau de jeu est composé de 7 colonnes et de 6 rangées de haut. On joue à chaque fois avec une couleur particulière (généralement jaune et rouge, ou noir et rouge).",
    "L’objectif du jeu est d’être le premier à obtenir 4 pions alignés horizontalement, verticalement ou en diagonale. Les nouveaux pions dans une colonne sont toujours placés au-dessus des autres pions ou sur la ligne des bas. Lorsqu'une colonne a 6 pièces, elle est pleine et il est impossible d'ajouter des pions supplémentaires. Si personne ne réussit à aligner 4 jetons et que toutes les colonnes sont pleines, la partie est nulle."
]
    
let dict_strategies = {
    "Contrôlez le centre": "Une stratégie simple pour augmenter vos chances de gagner au Puissance 4 consiste à placer des jetons au centre de la grille, car c’est là que vous aurez le plus d’opportunités pour faire des connexions. Étant donné qu’il y a un nombre impair de colonnes, si vous avez des jetons au centre, vous pourrez former des lignes dans tous les sens",
    "Prévoyez vos tours suivants": "Comme aux échecs, au Puissance 4, vous ou votre adversaire pouvez être obligés de placer un jeton de manière à empêcher l’autre de gagner. Vous pouvez parfois profiter de ces situations, il est donc important de réfléchir à la réaction de votre adversaire lorsque vous décidez où vous allez placer un jeton. Par exemple, si vous voulez être sûr de pouvoir mettre un jeton dans un trou particulier, vous pouvez placer des jetons qui pourraient potentiellement vous permettre de gagner ailleurs. Votre adversaire contrera votre attaque à cet endroit et vous pourrez glisser votre jeton dans l’emplacement que vous vouliez. Avant de jouer, demandez-vous comment votre adversaire pourrait bénéficier de votre coup. Vous ne voulez pas faire quelque chose qui pourrait lui permettre de gagner. Réfléchissez à la façon dont l’autre joueur pourra profiter de vos coups.",
    "Bloquez votre adversaire": "Dans n’importe quel jeu, la règle de base pour ne pas perdre est d’empêcher votre adversaire de gagner. Dans le cas de Puissance 4, cela signifie que vous devez vous défendre contre les tactiques de l’autre joueur en mettant vos jetons dans les trous libres dont il a besoin pour compléter une série de quatre . Lorsque c’est possible, empêchez votre adversaire de placer trois jetons en ligne continue, car dans ce cas, il ne lui manquera plus qu’un jeton pour gagner. De plus, en empêchant l’autre joueur de faire des séries de trois, vous l’empêcherez de vous piéger en mettant en place ses jetons de façon à pouvoir gagner dans plusieurs sens.",
    "Profitez des erreurs de l’autre joueur": "Dans ce jeu, si vous ne bloquez pas les coups de votre adversaire, vous lui permettrez de gagner. Pour éviter cela, soyez attentif à la disposition des jetons dans la grille et aux conséquences de chaque tour pour pouvoir profiter des éventuelles erreurs",
    "Ayez une stratégie offensive": "Il est important de vous défendre et de bloquer l’autre joueur, mais pour gagner, vous devez également former des séries avec vos propres jetons. Vous avez plusieurs possibilités pour cela. Formez des lignes horizontales en progressant vers l’extérieur. Empilez des jetons pour former des séries verticales. Utilisez vos jetons et ceux de votre adversaire pour former des séries diagonales entre les colonnes et les rangées. Lorsque c’est possible, mettez vos jetons dans des trous qui vous permettront d’établir des connexions dans plusieurs sens. Par exemple, si vous avez des jetons qui sont séparés par une colonne ou une rangée, trouvez un trou entre les deux qui vous permettra de commencer une série diagonale et horizontale ou verticale",
    "Faites attention aux trous vides": "Au Puissance 4, un espace libre à côté d’une série de trois jetons est un risque, car il peut permettre de gagner la partie. Parfois, ces trous ne peuvent pas être utilisés, car ceux qui se trouvent dessous sont vides. Évitez de mettre vos jetons dans les espaces qui se trouvent au-dessous, car votre adversaire pourrait s’en servir pour placer ses jetons aux bons endroits et gagner la partie. De même, si vous avez besoin de remplir un trou sous un autre pour pouvoir remporter la partie, n’y mettez pas un de vos propres jetons, car votre adversaire pourra simplement mettre un des siens dans l’espace dont vous avez besoin pour vous bloquer.",
    "Allez plus loin": "https://fr.wikihow.com/gagner-une-partie-de-Puissance-4#:~:text=Une%20strat%C3%A9gie%20simple%20pour%20augmenter,opportunit%C3%A9s%20pour%20faire%20des%20connexions."
}

let titres_strategies = Object.keys(dict_strategies)

let paragraphe = document.querySelector('p')

let titre = document.querySelector('#eitherRefOrStrat')

let btn_rules = document.querySelector('#back_rules')
let btn_strat = document.querySelector('#forward_strat')

btn_rules.addEventListener('click', afficher_reglements)
btn_strat.addEventListener('click', afficher_strategies)

/* 
Source: https://forum.freecodecamp.org/t/how-to-add-new-line-in-string/17763
Utilisation: changer le innerhtml du paragraphe avec une liste de string et integrer un bon breakline
User: camperbot
*/

function afficher_reglements() {
    let texte_reglement = liste_reglements.join("\n\n")
    paragraphe.innerHTML = texte_reglement
    btn_rules.style.visibility = 'hidden'
    btn_strat.style.visibility = 'visible'
    titre.innerText = "Reglements"
}

function afficher_strategies() {
    paragraphe.innerHTML = ''
    for (let i = 0; i < titres_strategies.length; i++){
        if (i === titres_strategies.length - 1){
            let titre = document.createElement('h3')
            titre.innerText = titres_strategies[i]
            let text = document.createElement('a')
            text.href = dict_strategies[titres_strategies[i]]
            text.innerText = "Plus de stratégies"
            paragraphe.append(titre, text)
        }
        else {
            let titre = document.createElement('h3')
            titre.innerText = titres_strategies[i]
            let text = document.createElement('p')
            text.innerText = dict_strategies[titres_strategies[i]]
            paragraphe.append(titre, text)
        }

    }
    btn_rules.style.visibility = 'visible'
    btn_strat.style.visibility = 'hidden'
    titre.innerText = "Strategies"
}

afficher_reglements()




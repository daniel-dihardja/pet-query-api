from langchain.schema import HumanMessage

MOCK_MESSAGES = {
    "de": [
        HumanMessage(
            content="Ich suche einen Kater, der eher zurückhaltend ist und sich vielleicht erst an Menschen gewöhnen muss. Es wäre ideal, wenn er später Freigang haben könnte, da ich in einer ruhigen Gegend wohne. Ich habe Geduld und würde ihm die Zeit geben, die er braucht, um Vertrauen aufzubauen."
        )
    ],
    "en": [
        HumanMessage(
            content="I am looking for a tomcat who is rather shy and might need some time to get used to people. It would be ideal if he could have outdoor access later, as I live in a quiet area. I am patient and would give him the time he needs to build trust."
        )
    ],
}

MOCK_PETS = [
    {
        "name": "Hr. Möckel",
        "type": "katze",
        "breed": "Hauskatze",
        "gender": "male",
        "neutered": 0,
        "birth_year": 2020,
        "image": "",
        "url": "",
        "text": "Herr Möckel kam als Fundtier ins Tierheim. Wir vermuten, daß der ehemals unkastrierte Kater sich früher auch der Straße durch schlagen musste. Dem Menschen gegenüber verhält er sich noch sehr zurückhaltend, aktuell lässt er sich noch nicht anfassen. Wir hoffen aber, dass er noch Vertrauen fassen wird. Herr Möckel hält sich bei uns vermehrt im Außenbereich auf, sodass wir für ihn ein Zuhause mit späteren Freigang suchen. Wenn Sie Interesse an einer unserer Katzen haben, kontaktieren Sie uns bevorzugt per E-Mail. Schildern Sie uns in der Mail, wie die Katze/die Katzen bei Ihnen leben wird/werden und senden Sie uns eine Telefonnummer zu. Es wird sich dann ein*e TierpflegerIn bei Ihnen melden. Info: Tierbeschreibungen basieren auf Beobachtungen im Tierheim oder auf Informationen Dritter und stellen keine zugesicherten Eigenschaften dar.",
    }
]

MOCK_PROBLEMATIC_DOGS = [
    {
        "id": "123",
        "name": "Sam",
        "type": "hund",
        "breed": "Schäferhund",
        "gender": "male",
        "neutered": 0,
        "birth_year": 2020,
        "image": "https://www.tierheim-leipzig.de/wp-content/uploads/2024/10/sam.jpg",
        "url": "https://www.tierheim-leipzig.de/Project/sam-2/",
        "text": "Sam wurde am 9.10.2023 als Einweisung auf der Grundlage des TierSchG zu uns ins Tierheim gebracht. Er zeigt sich oft unsicher und neigt bei Stresssituationen zu starkem Bellen und unkontrolliertem Verhalten. Mit der richtigen Führung könnte er jedoch ein treuer Begleiter werden.",
    },
    {
        "id": "456",
        "name": "Toni",
        "type": "hund",
        "breed": "Schäferhund-Mischling",
        "gender": "male",
        "neutered": 0,
        "birth_year": 2017,
        "image": "https://www.tierheim-leipzig.de/wp-content/uploads/2024/10/toni.jpg",
        "url": "https://www.tierheim-leipzig.de/Project/toni/",
        "text": "Toni erreichte uns über eine Sicherstellung aufgrund von TierSchG. Er hat ein dominantes Verhalten und braucht eine erfahrene Person, die ihm klare Grenzen setzen kann. Mit Geduld und Training zeigt er jedoch große Fortschritte.",
    },
    {
        "id": "789",
        "name": "Benny",
        "type": "hund",
        "breed": "Schäferhund-Mischling",
        "gender": "male",
        "neutered": 1,
        "birth_year": 2022,
        "image": "https://www.tierheim-leipzig.de/wp-content/uploads/2024/10/benny.jpg",
        "url": "https://www.tierheim-leipzig.de/Project/benny/",
        "text": "Benny ist ein aufgeregter und freundlicher Hund, der jedoch zu Hyperaktivität neigt. Er braucht klare Strukturen und ausreichend Bewegung, um sein überschüssiges Energielevel in den Griff zu bekommen.",
    },
]

MOCK_MESSAGES_FOR_PROBLEMATIC_DOGS = {
    "en": [
        HumanMessage(
            content="I am looking for a dog that might have behavioral issues or be considered difficult to handle. I am experienced with such dogs and willing to work with them."
        )
    ],
    "de": [
        HumanMessage(
            content="Ich suche einen Hund, der möglicherweise Verhaltensprobleme hat oder als schwierig zu handhaben gilt. Ich habe Erfahrung mit solchen Hunden und bin bereit, mit ihnen zu arbeiten."
        )
    ],
}

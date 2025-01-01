from langchain.schema import HumanMessage

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

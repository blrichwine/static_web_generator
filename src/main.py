from textnode import TextNode, TextType

def main():
    tn = TextNode("This is a text node", TextType.BOLD, "https://freepeoplereadfreely.org/")
    print(tn)

main()

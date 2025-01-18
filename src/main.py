from textnode import TextNode, TextType
from leafnode import LeafNode

def main():
    tn = TextNode("This is a text node", TextType.BOLD, "https://freepeoplereadfreely.org/")
    print(tn)

   
if __name__ == "__main__":
    main()

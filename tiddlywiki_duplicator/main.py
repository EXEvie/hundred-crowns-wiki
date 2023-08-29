import sys

from html_parser import WikiParser

if __name__ == '__main__':
    main_wiki_path = sys.argv[1]
    copy_wiki_path = sys.argv[2]

    main_wiki = WikiParser(main_wiki_path)
    copy_wiki = WikiParser(copy_wiki_path)

    copy_wiki.add_new_tiddlers_from_other_wiki(main_wiki)
    copy_wiki.write_to_file()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/

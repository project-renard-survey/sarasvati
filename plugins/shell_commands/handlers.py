import colored
from colored import stylize

__TITLE_STYLE = colored.fg("green")
__LINK_STYLE = colored.fg("blue") + colored.attr("underlined")
__DESC_STYLE = colored.fg("dark_gray")
__NOTHING_ERR = "No thought '{}' found to show."
__AMBIGUOUS_ERR = "Multiple thoughts ({}) found. Unable to show."


def ls(api, args):
    title = args.get("arg")
    search_result = api.brain.search.by_title(title, operator="~~")
    for thought in search_result:
        print(stylize(thought.title, __TITLE_STYLE), thought.description)


def show(api, args):
    title = args.get("arg")
    search = api.brain.search.by_title(title)
    thought = api.get_one(search,
                          __NOTHING_ERR.format(title),
                          __AMBIGUOUS_ERR.format(len(search)))

    print(stylize(thought.title, __TITLE_STYLE))
    print(thought.description)

    links = thought.links.all
    for thought in links:
        link = links[thought]
        print("{}: {} {}".format(link.kind.capitalize(),
                                 stylize(thought.title, __LINK_STYLE),
                                 stylize(thought.description, __DESC_STYLE)))

def quit_(api, args):
    print("Good bye, take care!")

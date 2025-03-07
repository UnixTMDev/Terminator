# Terminator module for getting information from the Pokédex

#Includes Eevee. Jank workaround.
eeveelutions = ["eevee","sylveon","espeon","umbreon","leafeon","glaceon","flareon","vaporeon","jolteon"]

import pokebase as dex
import webbrowser

def open_url(args: str) -> str:
    firefox = webbrowser.Mozilla("C:\\Program Files\\Mozilla Firefox\\firefox.exe")
    firefox.open_new(args)
    return

arg_format = "(summary/type/evolution/description/ID/name/ability) <pokemon name/national dex id>"
def pokedex(args: str) -> str:
    args.replace(";"," ")
    asdf = args.split(" ")
    try:
        if not asdf[1].isalpha():
            fdsa = int(asdf[1])
        else:
            fdsa = asdf[1].lower()
    except:
        fdsa = asdf[1].lower()
    if not asdf[0].lower() in "summary/type/evolution/description/entry/id/ability/abilities".split("/"):
        return "Invalid mode. Probably not the user's fault."
    try:
        mon = dex.pokemon(fdsa)
        species = dex.pokemon_species(asdf[1].lower())
        chain = species.evolution_chain

        match (asdf[0].lower()):
            # (summary/type/evolution/description/number/ability) <pokemon name>
            case "summary":
                evolve_message = ""
                if mon.name not in eeveelutions:
                    if len(chain.chain.evolves_to) == 0 or (chain.chain.evolves_to[-1].species.name == mon.name):
                        evolve_message = "This Pokémon can not evolve."
                    elif len(chain.chain.evolves_to) == 1:
                        evolve_message = f"This Pokémon evolves into {chain.chain.evolves_to[0].species.name.title()} via {chain.chain.evolves_to[0].evolution_details[0].trigger.name.replace('-',' ')}."
                    elif len(chain.chain.evolves_to) > 1:
                        evolve_message = f"This Pokémon's final evolution is {chain.chain.evolves_to[-1].species.name.title()}."

                if len(mon.types) <= 1:
                    Type = "a "+mon.types[0].type.name.title()
                else:
                    asdf = []
                    for x in mon.types:
                        asdf.append(x.type.name.title())
                    Type = "a "+"/".join(asdf)
                    del asdf

                return f"{mon.name.title()} has Pokédex ID {mon.id}, and is {Type} type. {evolve_message} It has the {'ability' if len(mon.abilities) == 1 else 'abilities'} {', '.join(x.ability.name for x in mon.abilities).title() if len(mon.abilities) > 1 else mon.abilities[0].ability.name.title()}."
            case "type":
                if len(mon.types) <= 1:
                    Type = "a "+mon.types[0].type.name.title()
                else:
                    asdf = []
                    for x in mon.types:
                        asdf.append(x.type.name.title())
                    Type = "a "+"/".join(asdf)
                    del asdf
                return f"{mon.name.title()} is {Type} type."
            case "evolution":
                evolve_message = ""
                if mon.name not in eeveelutions:
                    if len(chain.chain.evolves_to) == 0 or (chain.chain.evolves_to[-1].species.name == mon.name):
                        evolve_message = " can not evolve."
                    elif len(chain.chain.evolves_to) == 1:
                        evolve_message = f" evolves into {chain.chain.evolves_to[0].species.name.title()} via {chain.chain.evolves_to[0].evolution_details[0].trigger.name.replace('-',' ')}."
                    elif len(chain.chain.evolves_to) > 1:
                        evolve_message = f"'s final evolution is {chain.chain.evolves_to[-1].species.name.title()}."
                else:
                    evolve_message = "is special!"
                return f"{mon.name.title()}{evolve_message}"
            case "description" | 'entry':
                flavor_text = "ERROR GETTING DESCRIPTION."
                game_name = "ERROR GETTING GAME NAME"
                for x in species.flavor_text_entries[::-1]:
                    if x.language.name == "en":
                        flavor_text = x.flavor_text.replace("\n"," ")
                        game_name = x.version.name.title()
                return f"{mon.name.title()}'s Pokédex entry states (as of {game_name}): {flavor_text}"
            case "id":
                return f"{mon.name.title()} has Pokédex ID {mon.id}."
            case "ability" | 'abilities':
                return f"{mon.name.title()} has the {'ability' if len(mon.abilities) == 1 else 'abilities'} {', '.join(x.ability.name for x in mon.abilities).title() if len(mon.abilities) > 1 else mon.abilities[0].ability.name.title()}."
            case _:
                evolve_message = ""
                if mon.name not in eeveelutions:
                    if len(chain.chain.evolves_to) == 0 or (chain.chain.evolves_to[-1].species.name == mon.name):
                        evolve_message = "This Pokémon can not evolve."
                    elif len(chain.chain.evolves_to) == 1:
                        evolve_message = f"This Pokémon evolves into {chain.chain.evolves_to[0].species.name.title()} via {chain.chain.evolves_to[0].evolution_details[0].trigger.name.replace('-',' ')}."
                    elif len(chain.chain.evolves_to) > 1:
                        evolve_message = f"This Pokémon's final evolution is {chain.chain.evolves_to[-1].species.name.title()}."

                if len(mon.types) <= 1:
                    Type = "a "+mon.types[0].type.name.title()
                else:
                    asdf = []
                    for x in mon.types:
                        asdf.append(x.type.name.title())
                    Type = "a "+"/".join(asdf)
                    del asdf

                return f"{mon.name.title()} has Pokédex ID {mon.id}, and is {Type} type. {evolve_message} It has the {'ability' if len(mon.abilities) == 1 else 'abilities'} {', '.join(x.ability.name for x in mon.abilities).title() if len(mon.abilities) > 1 else mon.abilities[0].ability.name.title()}."
    except Exception as e:
        return f"There was an error: {str(type(e))}"
if __name__ == "__main__":
    desired = input("# ")
    print(pokedex(desired))

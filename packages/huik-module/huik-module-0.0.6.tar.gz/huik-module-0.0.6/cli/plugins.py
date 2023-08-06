import click
import os
import requests
from cli.utils import ColorText,TableDisplay
import json 
import math
import re


# plugin_folder = os.path.join(os.path.dirname(__file__), 'commands')

# class MyCLI(click.MultiCommand):
#     """
#     lazy load of sub commands from commands folder. 
#     """
#     commandList = {}
#     def list_commands(self, ctx):
#         rv = list(self.commandList.keys())
#         for filename in os.listdir(plugin_folder):
#             if filename.endswith('.py'):
#                 rv.append(filename[:-3])
#         rv.sort()
#         return rv

#     def get_command(self, ctx, name):
#         if name in self.commandList:
#             return self.commandList[name]
#         fn = os.path.join(plugin_folder, name + '.py')
#         ns = {'__file__':fn}
#         if os.path.isfile(fn):
#             with open(fn) as f:
#                 # code = compile(f.read(), fn, 'exec')
#                 exec(f.read(), ns, ns)
#             return ns['cli']
#         else:
#             return None

#     def add_command(self,f):
#         self.commandList[f.__name__] = f

#     def add_command(self, cmd, name=None):
#         """Registers another :class:`Command` with this group.  If the name
#         is not provided, the name of the command is used.
#         """
#         name = name or cmd.name
#         if name is None:
#             raise TypeError("Command has no name.")
#         if name in self.list_commands(1):
#             raise RuntimeError(f'Command {name} already exist.')
#         self.commandList[name] = cmd

#     def command(self, *args, **kwargs):
#         """A shortcut decorator for declaring and attaching a command to
#         the group.  This takes the same arguments as :func:`command` but
#         immediately registers the created command with this instance by
#         calling into :meth:`add_command`.
#         """
#         command = click.command

#         def decorator(f):
#             cmd = command(*args, **kwargs)(f)
#             self.add_command(cmd)
#             return cmd

#         return decorator

# # menu = MyCLI(help="Entry Point for other Commands",invoke_without_command=True)

# @click.group(cls=MyCLI,)
# @click.pass_context
# def plugins(ctx):
   
#     pass 




@click.group()
def plugins():
   
    pass 



APIs = os.path.join(os.path.dirname(__file__),'conf','api.json')
if not os.path.isfile(APIs):
    _=open(APIs,'wt')
    _.write("{}")
    _.close()

with open(APIs,'rt') as f:
    _data = json.load(f)
    COL_API_KEY=_data.get("COL_API_KEY",None)
    MED_API_KEY=_data.get("MED_API_KEY",None)
    URBAN_API_KEY=_data.get("URBAN_API_KEY",None)

def lookupMW(word,limit):
    url1=f"https://www.dictionaryapi.com/api/v3/references/collegiate/json/{word}?key={COL_API_KEY}"
    url2=f"https://www.dictionaryapi.com/api/v3/references/medical/json/{word}?key={MED_API_KEY}"
    try:
        if COL_API_KEY is None or (MED_API_KEY is None):
            raise ValueError ("Missing API key for M-W dictionary. Run def --config to setup.")
        r1 = requests.request("GET", url1, ).json()
        r2 = requests.request("GET", url2, ).json()
        def process(r):
            result = []
            for k,d in enumerate(r[0:limit]):
                if not isinstance(d,dict):
                    continue
                _def = [("<gDef {}.g> [{}]".format(k+1,d.get('fl','None')))]
                for i,l in enumerate(d.get('shortdef',[])):
                    _def.append(f"  [{i+1}]. {l}")
                result.append(_def)
            return result
        res1 = process(r1)
        res2 = process(r2)
        result = [["{From M-W Collegiate Dictionary}"]]+res1+[["{From M-W Medical Dictionary}"]]+res2

        return result
    except Exception as e:
        return e


def lookupUrban(word,limit):
    """
    look up word on urban dictionary, export a upper limit
    """
    url = "https://mashape-community-urban-dictionary.p.rapidapi.com/define"
    querystring = {"term":word}
    headers = {
        'x-rapidapi-host': "mashape-community-urban-dictionary.p.rapidapi.com",
        'x-rapidapi-key': URBAN_API_KEY
        }
    try:
        if URBAN_API_KEY is None:
            raise ValueError ("No API key for urban dictionary. Run def --config to setup.")
        response = requests.request("GET", url, headers=headers, params=querystring)
        r=response.json()
        result = []
        for k,d in enumerate(r['list'][0:limit]):
            _def = [("<gDef {}.g> {}".format(k+1,d.get('definition',"None")))]
            txt    =[f'<gExample:g>']
            exp = list((d.get('example',"None")).split('\n'))
            result.append(_def+txt+exp)
        return result
    except Exception as e:
        return e

def run_config():
    ck = click.prompt("Enter Key for M-W collegiate dictionary",default=COL_API_KEY)
    mk = click.prompt("Enter Key for M-W medical dictionary",default=MED_API_KEY)
    uk = click.prompt("Enter Key for Urban dictionary",default=URBAN_API_KEY)
    data = dict(COL_API_KEY=ck,MED_API_KEY=mk,URBAN_API_KEY=uk)
    click.echo('You have entered these keys:')
    click.echo(json.dumps(data,indent=4),)
    if click.confirm('Do you want to save?',abort=True,default=True):
        with open(APIs,'wt') as f:
            json.dump(data,f)

    click.echo('API keys are saved.')


@plugins.command('def')
@click.argument("word",nargs=-1)
@click.option('-u','--urban','-urban','dictionary',flag_value="urban",default=False,help="Use Urban Dictionary")
@click.option('-mw','--mw','-m','-mw','dictionary',flag_value="mw",default=True,help="Use M-W Dictionary")
@click.option("--dictionary",'-d',type=click.Choice(['mw',"urban"],case_sensitive=False),default='mw',help="Select M-W or Urban Dictionary")
@click.option("--limit",'-l',default=5,help="Limit explanation entries")
@click.option("--config",is_flag=True,help="Configure Dictionary API keys")
@click.pass_context
def _def(ctx,word,limit,dictionary,config):
    """
    Urban Dictionary or Merriam-Webster Dictionary.
    """
    if config:
        run_config()
        ctx.exit()
    if not word:
        click.echo(ctx.get_help())
        word = click.prompt('Please enter a word', type=str)
    else:
        word = " ".join(word)
    bkcolor = ColorText(mapping={"[]":"fC",("<g","g>") : "fG",("<alert>","</alert>"):"bR","{}":"bB"})
    if dictionary == "urban":
        result = lookupUrban(word,limit)
    else:
        result = lookupMW(word,limit)
    if isinstance(result,list) and result:
        td=TableDisplay(bkcolor)
        click.echo("")
        title = " DEFINITION : <g"+f">>> {word.capitalize()} <<<g>"
        click.echo(td.format(title=title,text=result))
        click.echo("")
    else:
        click.echo("")
        click.echo(bkcolor(f'<alert>!Unable to find online definition. \n <{result}> </alert>'))
        click.echo("")



@plugins.command()
@click.argument("inputs",nargs=-1)
@click.option('--precision','-p','precision',default='9g',help="Precision,9g/9e/9f",show_default=True)
def cal(inputs,precision):
    """
    A big calculator.
    """
    formula = "".join(inputs)
    # replace log and ln
    formula = re.sub( "log\s*(?P<num>\d+)" , "math.log10(\g<num>)" , formula)
    formula = re.sub( "log\s*\((?P<num>.*)\)" , "math.log10(\g<num>)" , formula)
    formula = re.sub( "ln\s*(?P<num>\d+)" , "math.log(\g<num>)" , formula)
    formula = re.sub( "ln\s*\((?P<num>.*)\)" , "math.log(\g<num>)" , formula)

    # replace constant e and pi
    formula = re.sub( "eu" , "math.e" , formula)
    formula = re.sub( "pi" , "math.pi" , formula)

    # replace ^ by **
    formula = re.sub( "\^" , "**" , formula)
    formula = re.sub( "sqrt" , "math.sqrt" , formula)
    formula = re.sub( "sin" , "math.sin" , formula)
    formula = re.sub( "cos" , "math.cos" , formula)
    formula = re.sub( "tan" , "math.tan" , formula)
    formula = re.sub( "asin" , "math.asin" , formula)
    formula = re.sub( "acos" , "math.acos" , formula)
    formula = re.sub( "atan" , "math.atan" , formula)
    formula = re.sub( "abs" , "math.fabs" , formula)

    # replace factorial inside parenthesis
    formula = re.sub("\((?P<num>.*)\)!","math.factorial(\g<num>)",formula,)
    # replace factorial of numbers
    formula = re.sub("(?P<num>\s*\d+\s*)!","math.factorial(\g<num>)",formula)
    try:
        result = eval(formula)
        result = [(f'  [结果] = {{:.{precision}}}').format(result)]

    except Exception as e:
        result = [f"Formula : {formula}" , '<alert>Error {} </alert>'.format(e)]
    line1 = f'  [计算] <f>{formula}</f>'
    bkcolor = ColorText(mapping={"[]":"fGsB",("<f>","</f>"):"fMsB","{}":"bB",("<alert>","</alert>"):"bR"})
    tf = TableDisplay(bkcolor)
    data = tf(title=bkcolor('{>>>计算器<<<}'),text=[[line1],result])
    click.echo('')
    click.echo(data)
    click.echo('')

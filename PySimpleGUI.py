#!/usr/bin/python3
import sys

if sys.version_info[0] >= 3:
    import tkinter as tk
    from tkinter import filedialog
    from tkinter.colorchooser import askcolor
    from tkinter import ttk
    import tkinter.scrolledtext as tkst
    import tkinter.font
else:
    import Tkinter as tk
    import tkFileDialog
    import ttk
    import tkColorChooser
    import tkFont
    import ScrolledText

import types
import datetime
import time
import pickle
import calendar
from random import randint
import textwrap
import operator
import inspect

#  888888ba           .d88888b  oo                     dP           .88888.  dP     dP dP
#  88    `8b          88.    "'                        88          d8'   `88 88     88 88
# a88aaaa8P' dP    dP `Y88888b. dP 88d8b.d8b. 88d888b. 88 .d8888b. 88        88     88 88
#  88        88    88       `8b 88 88'`88'`88 88'  `88 88 88ooood8 88   YP88 88     88 88
#  88        88.  .88 d8'   .8P 88 88  88  88 88.  .88 88 88.  ... Y8.   .88 Y8.   .8P 88
#  dP        `8888P88  Y88888P  dP dP  dP  dP 88Y888P' dP `88888P'  `88888'  `Y88888P' dP
#                 .88                         88
#             d8888P                          dP


g_time_start = 0
g_time_end = 0
g_time_delta = 0


def TimerStart():
    """ """
    global g_time_start

    g_time_start = time.time()


def TimerStop():
    """ """
    global g_time_delta, g_time_end

    g_time_end = time.time()
    g_time_delta = g_time_end - g_time_start
    print((g_time_delta * 1000))


"""
    Welcome to the "core" PySimpleGUI code....

    It's a mess.... really... it's a mess internally... it's the external-facing interfaces that
    are not a mess.  The Elements and the methods for them are well-designed.
    PEP8 - this code is far far from PEP8 compliant. 
    It was written PRIOR to learning that PEP8 existed. 

    I'll be honest.... started learning Python in Nov 2017, started writing PySimpleGUI in Feb 2018.
    Released PySimpleGUI in July 2018.  I knew so little about Python that my parameters were all named
    using CamelCase.  DOH!  Someone on Reddit set me straight on that.  So overnight I renamed all of the
    parameters to lower case.  Unfortunately, the internal naming conventions have been set.  Mixing them
    with PEP8 at this moment would be even MORE confusing.

    Code I write now, outside PySimpleGUI, IS PEP8 compliant.  

    The variable and function naming in particular are not compliant.  There is
    liberal use of CamelVariableAndFunctionNames.  If you've got a serious enough problem with this
    that you'll pass on this package, then that's your right and I invite you to do so.  However, if
    perhaps you're a practical thinker where it's the results that matter, then you'll have no
    trouble with this code base.  There is consisency however.  

    I truly hope you get a lot of enjoyment out of using PySimpleGUI.  It came from good intentions.
"""

# ----====----====----==== Constants the user CAN safely change ====----====----====----#

# Base64 encoded GIF file
DEFAULT_BASE64_ICON = b'R0lGODlhIQAgAPcAAAAAADBpmDBqmTFqmjJrmzJsnDNtnTRrmTZtmzZumzRtnTdunDRunTRunjVvnzdwnzhwnjlxnzVwoDZxoTdyojhzozl0ozh0pDp1pjp2pjp2pzx0oj12pD52pTt3qD54pjt4qDx4qDx5qTx5qj16qj57qz57rD58rT98rkB4pkJ7q0J9rEB9rkF+rkB+r0d9qkZ/rEl7o0h8p0x9pk5/p0l+qUB+sEyBrE2Crk2Er0KAsUKAskSCtEeEtUWEtkaGuEiHuEiHukiIu0qKu0mJvEmKvEqLvk2Nv1GErVGFr1SFrVGHslaHsFCItFSIs1COvlaPvFiJsVyRuWCNsWSPsWeQs2SQtGaRtW+Wt2qVuGmZv3GYuHSdv3ievXyfvV2XxGWZwmScx2mfyXafwHikyP7TPP/UO//UPP/UPf/UPv7UP//VQP/WQP/WQf/WQv/XQ//WRP7XSf/XSv/YRf/YRv/YR//YSP/YSf/YSv/ZS//aSv/aS/7YTv/aTP/aTf/bTv/bT//cT/7aUf/cUP/cUf/cUv/cU//dVP/dVf7dVv/eVv/eV//eWP/eWf/fWv/fW/7cX/7cYf7cZP7eZf7dav7eb//gW//gXP/gXf/gXv/gX//gYP/hYf/hYv/iYf/iYv7iZP7iZf/iZv/kZv7iaP/kaP/ka//ma//lbP/lbv/mbP/mbv7hdP7lcP/ncP/nc//ndv7gef7gev7iff7ke/7kfv7lf//ocf/ocv/odP/odv/peP/pe//ofIClw4Ory4GszoSszIqqxI+vyoSv0JGvx5OxyZSxyZSzzJi0y5m2zpC10pi715++16C6z6a/05/A2qHC3aXB2K3I3bLH2brP4P7jgv7jh/7mgf7lhP7mhf7liv/qgP7qh/7qiP7rjf7sjP7nkv7nlv7nmP7pkP7qkP7rkv7rlv7slP7sl/7qmv7rnv7snv7sn/7un/7sqv7vq/7vrf7wpv7wqf7wrv7wsv7wtv7ytv7zvP7zv8LU48LV5c3a5f70wP7z0AAAACH5BAEAAP8ALAAAAAAhACAAAAj/AP8JHEiwoMGDCA1uoYIF4bhK1vwlPOjlQICLApwVpFTGzBk1siYSrCLgoskFyQZKMsOypRyR/GKYnBkgQbF/s8603KnmWkIaNIMaw6lzZ8tYB2cIWMo0KIJj/7YV9XgGDRo14gpOIUBggNevXpkKGCDsXySradSoZcMmDsFnDxpEKEC3bl2uXCFQ+7emjV83bt7AgTNroJINAq0wWBxBgYHHdgt0+cdnMJw5c+jQqYNnoARkAx04kPEvS4PTqBswuPIPUp06duzcuYMHT55wAjkwEahsQgqBNSQIHy582D9BePTs2dOnjx8/f1gJ9GXhRpTqApFQoDChu3cOAps///9D/g+gQvYGjrlw4cU/fUnYX6hAn34HgZMABQo0iJB/Qoe8UxAXOQiEg3wIXvCBQLUU4mAhh0R4SCLqJOSEBhhqkAEGHIYgUDaGICIiIoossogj6yBUTQ4htNgiCCB4oIJAtJTIyI2MOOLIIxMtQQIJIwQZpAgwCKRNI43o6Igll1ySSTsI7dOECSaUYOWVKwhkiyVMYuJlJpp0IpA6oJRTkBQopHnCmmu2IBA2mmQi5yZ0fgJKPP+0IwoooZwzkDQ2uCCoCywUyoIW/5DDyaKefOLoJ6LU8w87pJgDTzqmDNSMDpzqYMOnn/7yTyiglBqKKKOMUopA7JgCy0DdeMEjUDM71GqrrcH8QwqqqpbiayqToqJKLwN5g45A0/TAw7LL2krGP634aoopp5yiiiqrZLuKK+jg444uBIHhw7g+MMsDFP/k4wq22rririu4xItLLriAUxAQ5ObrwzL/0PPKu7fIK3C8uxz0w8EIIwzMP/cM7HC88hxEzBBCBGGxxT8AwQzDujws7zcJQVMEEUKUbPITAt1D78OSivSFEUXEXATKA+HTscC80CPSQNGEccQRYhjUDzfxcjPPzkgnLVBAADs='

DEFAULT_BASE64_LOADING_GIF = b'R0lGODlhQABAAKUAAAQCBJyenERCRNTS1CQiJGRmZLS2tPTy9DQyNHR2dAwODKyqrFRSVNze3GxubMzKzPz6/Dw6PAwKDKSmpExKTNza3CwqLLy+vHx+fBQWFLSytAQGBKSipERGRNTW1CQmJGxqbLy6vPT29DQ2NHx6fBQSFKyurFRWVOTi5HRydPz+/Dw+PP7+/gAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACH/C05FVFNDQVBFMi4wAwEAAAAh+QQJCQAsACwAAAAAQABAAAAG/kCWcEgsGo/IpHLJbDqf0CjxwEmkJgepdrvIAL6A0mJLdi7AaMC4zD4eSmlwKduuCwNxdMDOfEw4D0oOeWAOfEkmBGgEJkgphF8ph0cYhCRHeJB7SCgJAgIJKFpnkGtTCoQKdEYGEmgSBlEqipAEEEakcROcqGkSok8PkGCBRhNwcrtICYQJUJnDm0YHASkpAatHK4Qrz8Nf0mTbed3B3wDFZY95kk8QtIS2bQ29r8BPE8PKbRquYBuxpJCwdKhBghUrQpFZAA8AgX2T7DwIACiixYsYM2rc+OSAhwrZOEa5QGHDlw0dLoiEAqEAoQK3VjJxCQmEzCUhzgXciOKE/gIFJ+4NEXBOAEcPyL6UqEBExLkvIjYyiMOAyICnAAZs9IdGgVWsWjWaTON1yAGsUTVOTUOhyLhh5TQi7cqUyIVzKjmiYCBBQtAjNAnZvKmk5cuYhJVc6DAWZd7ETTx6CAm5suXLRQY4sPDTQoqwmIlAADE2DYi0oUUQhbQC8WUQ5wZf9oDVA58KdaPAflqgTgMEXxA0iPIB64c6I9AgiFL624Y2FeLkbtJ82HM2tNPYfmLBOHLlUQJ/6z0POADhUa4+3V7HA/vw58gfEaFBA+qMIt6Su9/UPAL+F4mwWxwwJZGLGitp9kFfHzgAGhIHmhKaESIkB8AIrk1YBAQmDJiQoYYghijiiFAEAQAh+QQJCQApACwAAAAAQABAAIUEAgSEgoREQkTU0tRkYmQ0MjSkpqTs6ux0cnQUEhSMjozc3ty0trT09vRUUlRsamw8OjwMCgxMSkx8fnwcGhyUlpTk5uS8vrz8/vwEBgSMioxERkTc2txkZmQ0NjS0srT08vR0dnQUFhSUkpTk4uS8urz8+vxsbmw8Pjz+/v4AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAG/sCUcEgsGo/IpHLJbDqf0Kh0Sl0aPACAx1DtOh/ZMODhLSMNYjHXzBZi01lPm42BizHz5CAk2YQGSSYZdll4eUUYCHAhJkhvcAWHRiGECGeEa0gNAR4QEw1TA4RZgEcdcB1KBwViBQdSiqOWZ6wABZlIE3ATUhujAAJsj2FyUQK/wWbDcVInvydsumm8UaKjpWWrra+whNBtDRMeHp9UJs5pJ4aSXgMnGxsI2Oz09fb3+Pn6+/xEJh8KRjBo1M/JiARiEowoyIQAIQIMk1T4tXAfBw6aEI5KAArfgjcFFhj58CsLg3zDIhXRUBKABnwc4GAkoqDly3vWxMxLQbLk/kl8tbKoJAJCIyGO+RbUCnlkxC8F/DjsLOLQDsSISRREEBMBKlYlDRgoUMCg49ezaNOqVQJCqtm1Qy5IGAQgw4YLcFOYOGWnA8G0fAmRSVui5c+zx0omM2NBgwYLUhq0zPKWSIMFHCojsUAhiwjIUHKWnPpBAF27H5YEEBOg2mQA80A4ICQBRBJpWVpDAfHabAMUv1BoFkJChGcSUoCXREGEUslZRxoHAB3lQku8Qg7Q/ZWB26HAdgYLmTi5Aru9hPwSqdryKrsLG07fNTJ7soN7IAZwsH2EfUn3ETk1WUVYWbDdKBlQh1Usv0D3VQPLpOHBcAyBIAFt/K31AQrbBqGQWhtBAAAh+QQJCQAyACwAAAAAQABAAIUEAgSEgoTEwsREQkTk4uQsLiykoqRkYmQUEhTU0tRUUlT08vS0srSMjox8enwMCgzMysw8OjwcGhxcWlz8+vy8urxMSkzs6uysqqxsamzc2tyUlpQEBgSMiozExsTk5uQ0NjSkpqRkZmQUFhRUVlT09vS0trSUkpR8fnwMDgzMzsw8PjwcHhxcXlz8/vy8vrxMTkzc3tz+/v4AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAG/kCZcEgsGo/IpHLJbDqf0Kh0Sq1ar8nEgMOxqLBgZCIFKAMeibB6aDGbB2u1i+Muc1xxJSWmoSwpdHUcfnlGJSgIZSkoJUptdXCFRRQrdQArhEcqD24PX0wUmVMOlmUOSiqPXkwLLQ8PLQtTFCOlAAiiVyRuJFMatmVpYIB1jVEJwADCWCWBdsZQtLa4artmvaO2p2oXrhyxVCWVdSvQahR4ViUOZAApDuaSVhQaGvHy+Pn6+/z9/v8AAzrxICJCBBEeBII6YOnAPYVDWthqAfGIgGQC/H3o0OEDEonAKPL7IKHMCI9GQCQD0S+AmwBHVAJjyQ/FyyMgJ/YjUAvA/ggCFjFqDNAxSc46IitOOlqmRS6lQwSIABHhwAuoWLNq3cq1ogcHLVqgyFiFAoMGJ0w8teJBphsQCaWcaFcGwYkwITiV4hAiCsNSB7B4cLYXwpMNye5WcVEgWZkC6ZaUSAQMwUMnFRybqdCEgWYTVUhpBrBtSQfNHZC48BDCgIfIRKxpxrakAWojLjaUNCNhA2wZsh3TVuLZMWgiJRTYgiFKtObSShbQLZUinohkIohkHs25yYnERVRo/iSDQmPHBdYi+Wsp6ZDrjrNH1Uz2SYPpKRocOZ+sQJEQhLnBgQFTlHBWAyZcxoJmEhjRliVw4cMfMP4ZQYEADpDQggMvJ/yWB3zYYQWBZnFBxV4p8mFVAgzLqacQBSf0ZNIJLla0mgGu1ThFEAAh+QQJCQAqACwAAAAAQABAAIUEAgSUkpRERkTMyswkIiTs6uy0trRkZmQ0MjTU1tQcGhykpqRUVlT09vTEwsQsKix8enwMCgycnpzU0tS8vrw8Ojzc3txcXlz8/vwEBgSUlpRMSkzMzswkJiT08vS8urxsamw0NjTc2twcHhysqqz8+vzExsQsLix8fnxkYmT+/v4AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAG/kCVcEgsGo/IpHLJbDqf0Kh0Sq1ar8tEAstdWk4AwMnSLRfBYbF5nUint+tu2w2Ax5OFghMdPt2TBg9hDwZMImgnIn9HH3QAhUxaTw0LCw1WHY4dax6CAA8eVAWOYXplEm4SoqQApl2oaapUmXSbZgW0HaFUBo6QZpQLu1UGub+LWHnIy8zNzs/Q0dLTzSYQFxcoDtRMAwiOCCZJDRwDl88kGawZC0YlEOoAGRDnywPx6wNEHnxpJ8N/SvRjdaLEkAOsDiyjwMrRByEe8NHJADAOhIZ0IAgZgFHcIgYY3TAQYqIjMpAhw4xUEXFdxTUXUwLQKAQhKYXIGsl8CHGg/piXa0p4wvgAA5EG8MLMq4esZEiPRRoMMMGU2QKJbthxQ2LiG51wW5NgcACBwQUIFIyGXcu2bdgGGjZ06LBBQ1UoJg5UqHAAKhcTBByN8OukRApHKe5OcYA1TQbCTC6wuoClQeCGIxQjcYBxm5UAKQM8kdyQshUBKQU8CYERwZURKUc88crKNZIJZRlAmIAEdkjZTkhPPtLAppsDd1GHVO2Ec0PPREoodyTAIBHQIUWPHm5EA0btQxoowKgAaJISwtNcsF7ENyvgRCg0Vgq5iYMDISqkoIDEQkoyRZjgXhojQHcHRyHpYwRcAhBAgAB2LeNfSACyNaBgbqngXUPgGLElHSvVZahCA4fRcYFma3GQGwQciAhNEAAh+QQJCQAwACwAAAAAQABAAIUEAgSEgoTEwsRERkTk4uQkIiSkpqRsamwUEhTU0tT08vSUkpRUUlQ0MjS0trQMCgzMyszs6ux8enwcGhzc2tz8+vyMioxMTkysrqw8OjwEBgSEhoTExsRMSkzk5uQkJiSsqqxsbmwUFhTU1tT09vSUlpRUVlQ0NjS8vrwMDgzMzszs7ux8fnwcHhzc3tz8/vz+/v4AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAG/kCYcEgsGo/IpHLJbDqf0Kh0Sq1ar9hs1sNiebRgowsBACBczJcKA1K9wkxWucxSVgKTOUC0qcCTcnN1SBEnenoZX39iZAApaEcVhod6J35SFSgoJE4EXYpHFpSUAVIqBWUFKlkVIqOHIpdOJHlzE5xXEK+UHFAClChYBruHBlAowMLEesZPtHoiuFa6y2W9UBAtZS2rWK3VsVIkmtJYosuDi1Ekk68n5epPhe4R8VR3rnN8svZTLxAg2vDrR7CgwYMItZAo0eHDhw4l4CVMwgHVoRbXjrygMOLNQQEaXmnISARErQnNCFbQtqsFPBCUUtpbUG0BkRe19EzwaG9A/rUBREa8GkHQIrEWRCgMJcjyKJFvsHjG87kMaMmYBWkus1nEwEmZ9p7tmqBA44gRA/uhCDlq5MQlHJrOaSHgLZOFAwoUGBDRrt+/gAMLhkMiwYiyV0iogCARCwUTbDWYoHBPQmQJjak4eEDpgQMpKxpQarAiCwXOox4QhXLg1YEsDIgxgKKALSUNiKvUXpb5CLVXJKeoqNatCQdiwY2QyH0kAfEnu9syJ0Jiw4dUGxorqNb7SOtRr4+saDeH9BETsqOEHl36yIVXF46MQN15NRQSlstowIzk+K7kMGzW2WdUKAABB90FQEwp8l1g2wX2xfOda0oolkB3YWyw4GBCIfgHHIdCvDdKByAKsd4h5pUIAwkBsNRCdioWoUB7MRoUBAAh+QQJCQAuACwAAAAAQABAAIUEAgSEhoTMzsxMSkykpqQcHhz08vRkYmQUEhSUlpS0trTc3twsLixsbmwMCgzU1tSsrqz8+vycnpyMjoxUUlQkJiRsamwcGhy8vrw0NjR0dnQEBgTU0tSsqqz09vRkZmQUFhScmpy8urzk5uQ0MjR0cnQMDgzc2ty0srT8/vykoqSUkpRUVlQsKiz+/v4AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAG/kCXcEgsGo8RRWlAaSgix6h0Sp2KKoCstiKqer/fkHasTYDP6KFoQ25303BqBNsmV6DxvBFSr0P0gEMNfW0WgYEDhGQDRwsTFhYTC4dTiYpajEQeB2xjBx6URxaXWoZDHiR9JKChRHykAH9DB4oHcQIlJQJRc6R3Qwukk2gcnRscUSKkb0ITpBNpo6VSCZ11ZkS0l7Zo0lmmUQp0YxUKRtq1aQLGyFNJDUxOeEXOl9DqDbqhJ6QnrYDo6nD7l8cDgz4MWBHMYyBglgMGFh46MeHDhwn+JGrcyLGjx48gO3rg8CBiSDQnWBhjkfFkFQUO2jgwF8UACgUmPz6IWcfB/oMjGBBkQYABJAVFFIwYMDEGQc6NBqz1USjk1RhZHAWQ2kUERRsUHrVe4jpk6RgTTzV6IEVVCAamAEwU/XiUUNIjNlGk5bizj0+XVGDKpAl4yoO6WSj8LOzFgwAObRlLnky5suXLEg2o0FCCwF40KU48SEGwg1AtCDrk6XAhywUCrTr0UZ1GNhnYhwycbuMUdGsyF0gHkqBIApoHfRYDKqGoAcrkhzQoKoEmAog2IIRHSSEiQAAR84wQJ2Qcje0xuKOcaDGmhfIiZuughUPg9+spI66TATEiyvnbeaTwwAPhidLHB1IQsBsACKS3kX7YTWGABLlI8BlBEShSIGUQIO6HmRDekIHgh/lh19+HLjzA3hbvfZiEdwpoh+KMjAUBACH5BAkJACYALAAAAABAAEAAhQQCBISGhMzKzERCRDQyNKSmpOzq7GRiZBQSFHRydJyanNTW1LS2tPz6/Dw6PAwODLSytPTy9GxubBweHHx6fKSipNze3AQGBIyKjMzOzExOTDQ2NKyqrOzu7GRmZBQWFHR2dJyenNza3Ly+vPz+/Dw+PP7+/gAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAb+QJNwSCwaj8ikcslsmjoYx+fjwHSc2KyS8QF4vwiGdjxmXL5or5jMXnYQ6TTi2q4bA/F4wM60UDZTGxQWRw55aRt8SSQUhyAkRQ+HaA+KRw0akwAaDUSSmgCVRg0hA1MDCp1ZIKAACUQbrYlFBrGIBlgirV4LQ3ige0QNtnEbqkwSuwASQ2+aD3RDCpoKTgTKBEQMmmtEhpMlTp+tokMMcGkP3UToh+VL46DvQh0BGwgIGwHRkc/W2HW+HQrXJNkuZm2mTarWZIGyXm2GHTKGhRWoV3ZqFcOFBZMmTooaKCiBr0SqMQ0sxgFxzJIiESAI4CMAQoTLmzhz6tzJs6f+z59Ah0SoACJBgQhByXDoAoZD0iwcDjlFIuDAAQFPOzCNM+dIhjMALmRIGkJTiCMe0BxIavAQwiIH1CZNoAljka9exJI1iySDVaxJneV5gPQpk6h5Chh2UqAdAASKFzvpEKJoCH6SM2vezLmz58+gQ7fhsOHCBQeR20SAwKDwzbZf3o4ZgQ7BiJsFDqXOEiFeV0sCEZGBEGcqHxKaIGkhngaCJRJg41xQnkWwF8IuiQknM+LTg9tMBAQIADhJ7sRtOrDGfIRE3C8HWhqB7UV2Twx6lhQofWHDbp8TxDGBaEIgl4d8nwWYxoAEmvALGsEQ6J5aCIYmHnkNZqghgUEBAAAh+QQJCQAnACwAAAAAQABAAIUEAgSEgoRERkTEwsTk4uRkYmQ0MjQUFhRUVlTU1tT08vSkpqQMCgxMTkzMysxsbmz8+vzs6uwcHhxcXlzc3tysrqwEBgSEhoRMSkzExsRkZmQ8OjwcGhxcWlzc2tz09vSsqqwMDgxUUlTMzsx0dnT8/vzs7uz+/v4AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAG/sCTcEgsGo/IpHLJbA5NjozJSa02RxiAFiAYWb/g08Ky3VoW4TRzxCiXLV613Jh1lwVzJ4RCgCQjdnZTeUkZImQAFiIZRxmBbgOERyUkjyQlRQOPZZFIFCAVHmGVmyRFgJtag0UUAncUVpqpAJ1Drpt4RhQHdgewVHWpGEUOiHZwR7d2uU0fbbMWfkRjx2hGHqkJTtizWqLEylwOSAup1kzc3d9GERlSShWpIE4fxpvRaumB2k7BuHPh7lSRlapWml29flEhZYkQARF31lGBwNANCWmEPIAAwS9MhgaILDQwKEnSHgoYS6pcqRJCSpZzMhTgBeBAAZIwrXzo8AjB/oecXxQYSGVgFdAmCLohODoEhAELFjacE+KoGy2mD+w8IJLU6lKgIB6d42C15tENjwwMKatFQc4SqTCdYAvALcwS9t7IpdntwNGhgdQK4en1aNhA5wjOwrkyq5utXJUyFbLgqQUDU4UIJWp3MhMFXe0gMOqZyYAJZAFwmMC4dBMIP13Lnk27tu3buHPnSYABKoaOYRwUKMBIZYJnWhgAtzIiZBxJ/rQw+6KhTIGSEPImkvulgPWSeI+9pNJcC7KS0bmoGTFhwnNJx8sod10BAYIKTRLcErD86IUyAeiGhAn2WECagCeMYMd7CJ5A4BsHIhgAgA0eUd99FWao4YYcAy4RBAA7OEloRWRqYW9jdzhOTjdUeHV4MTVCcmpRRWxDKzdGSWtiWnV5UUlCY0t5QTlKYmUzU25OM3ArSDd0K3JOMEtOTw=='

PSG_DEBUGGER_LOGO = b'R0lGODlhMgAtAPcAAAAAADD/2akK/4yz0pSxyZWyy5u3zZ24zpW30pG52J250J+60aC60KS90aDC3a3E163F2K3F2bPI2bvO3rzP3qvJ4LHN4rnR5P/zuf/zuv/0vP/0vsDS38XZ6cnb6f/xw//zwv/yxf/1w//zyP/1yf/2zP/3z//30wAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACH5BAEAAP8ALAAAAAAyAC0AAAj/AP8JHEiwoMGDCBMqXMiwoUOFAiJGXBigYoAPDxlK3CigwUGLIAOEyIiQI8cCBUOqJFnQpEkGA1XKZPlPgkuXBATK3JmRws2bB3TuXNmQw8+jQoeCbHj0qIGkSgNobNoUqlKIVJs++BfV4oiEWalaHVpyosCwJidw7Sr1YMQFBDn+y4qSbUW3AiDElXiWqoK1bPEKGLixr1jAXQ9GuGn4sN22Bl02roo4Kla+c8OOJbsQM9rNPJlORlr5asbPpTk/RP2YJGu7rjWnDm2RIQLZrSt3zgp6ZmqwmkHAng3ccWDEMe8Kpnw8JEHlkXnPdh6SxHPILaU/dp60LFUP07dfRq5aYntohAO0m+c+nvT6pVMPZ3jv8AJu8xktyNbw+ATJDtKFBx9NlA20gWU0DVQBYwZhsJMICRrkwEYJJGRCSBtEqGGCAQEAOw=='

DEFAULT_WINDOW_ICON = DEFAULT_BASE64_ICON

DEFAULT_ELEMENT_SIZE = (45, 1)  # In CHARACTERS
DEFAULT_BUTTON_ELEMENT_SIZE = (10, 1)  # In CHARACTERS
DEFAULT_MARGINS = (10, 5)  # Margins for each LEFT/RIGHT margin is first term
DEFAULT_ELEMENT_PADDING = (5, 3)  # Padding between elements (row, col) in pixels
DEFAULT_AUTOSIZE_TEXT = True
DEFAULT_AUTOSIZE_BUTTONS = True
DEFAULT_FONT = ("Helvetica", 10)
DEFAULT_TEXT_JUSTIFICATION = 'left'
DEFAULT_BORDER_WIDTH = 1
DEFAULT_AUTOCLOSE_TIME = 3  # time in seconds to show an autoclose form
DEFAULT_DEBUG_WINDOW_SIZE = (80, 20)
DEFAULT_WINDOW_LOCATION = (None, None)
MAX_SCROLLED_TEXT_BOX_HEIGHT = 50
DEFAULT_TOOLTIP_TIME = 400
DEFAULT_TOOLTIP_OFFSET = (0, -20)
#################### COLOR STUFF ####################
BLUES = ("#082567", "#0A37A3", "#00345B")
PURPLES = ("#480656", "#4F2398", "#380474")
GREENS = ("#01826B", "#40A860", "#96D2AB", "#00A949", "#003532")
YELLOWS = ("#F3FB62", "#F0F595")
TANS = ("#FFF9D5", "#F4EFCF", "#DDD8BA")
NICE_BUTTON_COLORS = ((GREENS[3], TANS[0]),
                      ('#000000', '#FFFFFF'),
                      ('#FFFFFF', '#000000'),
                      (YELLOWS[0], PURPLES[1]),
                      (YELLOWS[0], GREENS[3]),
                      (YELLOWS[0], BLUES[2]))

COLOR_SYSTEM_DEFAULT = '1234567890'  # Colors should never be this long
if sys.platform == 'darwin':
    DEFAULT_BUTTON_COLOR = COLOR_SYSTEM_DEFAULT  # Foreground, Background (None, None) == System Default
    OFFICIAL_PYSIMPLEGUI_BUTTON_COLOR = COLOR_SYSTEM_DEFAULT  # Colors should never be this long
else:
    DEFAULT_BUTTON_COLOR = ('white', BLUES[0])  # Foreground, Background (None, None) == System Default
    OFFICIAL_PYSIMPLEGUI_BUTTON_COLOR = ('white', BLUES[0])  # Colors should never be this long

DEFAULT_ERROR_BUTTON_COLOR = ("#FFFFFF", "#FF0000")
DEFAULT_BACKGROUND_COLOR = None
DEFAULT_ELEMENT_BACKGROUND_COLOR = None
DEFAULT_ELEMENT_TEXT_COLOR = COLOR_SYSTEM_DEFAULT
DEFAULT_TEXT_ELEMENT_BACKGROUND_COLOR = None
DEFAULT_TEXT_COLOR = COLOR_SYSTEM_DEFAULT
DEFAULT_INPUT_ELEMENTS_COLOR = COLOR_SYSTEM_DEFAULT
DEFAULT_INPUT_TEXT_COLOR = COLOR_SYSTEM_DEFAULT
DEFAULT_SCROLLBAR_COLOR = None
# DEFAULT_BUTTON_COLOR = (YELLOWS[0], PURPLES[0])    # (Text, Background) or (Color "on", Color) as a way to remember
# DEFAULT_BUTTON_COLOR = (GREENS[3], TANS[0])    # Foreground, Background (None, None) == System Default
# DEFAULT_BUTTON_COLOR = (YELLOWS[0], GREENS[4])    # Foreground, Background (None, None) == System Default
# DEFAULT_BUTTON_COLOR = ('white', 'black')    # Foreground, Background (None, None) == System Default
# DEFAULT_BUTTON_COLOR = (YELLOWS[0], PURPLES[2])    # Foreground, Background (None, None) == System Default
# DEFAULT_PROGRESS_BAR_COLOR = (GREENS[2], GREENS[0])     # a nice green progress bar
# DEFAULT_PROGRESS_BAR_COLOR = (BLUES[1], BLUES[1])     # a nice green progress bar
# DEFAULT_PROGRESS_BAR_COLOR = (BLUES[0], BLUES[0])     # a nice green progress bar
# DEFAULT_PROGRESS_BAR_COLOR = (PURPLES[1],PURPLES[0])    # a nice purple progress bar

# A transparent button is simply one that matches the background
TRANSPARENT_BUTTON = ('#F0F0F0', '#F0F0F0')
# --------------------------------------------------------------------------------
# Progress Bar Relief Choices
RELIEF_RAISED = 'raised'
RELIEF_SUNKEN = 'sunken'
RELIEF_FLAT = 'flat'
RELIEF_RIDGE = 'ridge'
RELIEF_GROOVE = 'groove'
RELIEF_SOLID = 'solid'

DEFAULT_PROGRESS_BAR_COLOR = (GREENS[0], '#D0D0D0')  # a nice green progress bar
DEFAULT_PROGRESS_BAR_SIZE = (20, 20)  # Size of Progress Bar (characters for length, pixels for width)
DEFAULT_PROGRESS_BAR_BORDER_WIDTH = 1
DEFAULT_PROGRESS_BAR_RELIEF = RELIEF_GROOVE
PROGRESS_BAR_STYLES = ('default', 'winnative', 'clam', 'alt', 'classic', 'vista', 'xpnative')
DEFAULT_PROGRESS_BAR_STYLE = 'default'
DEFAULT_METER_ORIENTATION = 'Horizontal'
DEFAULT_SLIDER_ORIENTATION = 'vertical'
DEFAULT_SLIDER_BORDER_WIDTH = 1
DEFAULT_SLIDER_RELIEF = tk.FLAT
DEFAULT_FRAME_RELIEF = tk.GROOVE

DEFAULT_LISTBOX_SELECT_MODE = tk.SINGLE
SELECT_MODE_MULTIPLE = tk.MULTIPLE
LISTBOX_SELECT_MODE_MULTIPLE = 'multiple'
SELECT_MODE_BROWSE = tk.BROWSE
LISTBOX_SELECT_MODE_BROWSE = 'browse'
SELECT_MODE_EXTENDED = tk.EXTENDED
LISTBOX_SELECT_MODE_EXTENDED = 'extended'
SELECT_MODE_SINGLE = tk.SINGLE
LISTBOX_SELECT_MODE_SINGLE = 'single'

TABLE_SELECT_MODE_NONE = tk.NONE
TABLE_SELECT_MODE_BROWSE = tk.BROWSE
TABLE_SELECT_MODE_EXTENDED = tk.EXTENDED
DEFAULT_TABLE_SECECT_MODE = TABLE_SELECT_MODE_EXTENDED

TITLE_LOCATION_TOP = tk.N
TITLE_LOCATION_BOTTOM = tk.S
TITLE_LOCATION_LEFT = tk.W
TITLE_LOCATION_RIGHT = tk.E
TITLE_LOCATION_TOP_LEFT = tk.NW
TITLE_LOCATION_TOP_RIGHT = tk.NE
TITLE_LOCATION_BOTTOM_LEFT = tk.SW
TITLE_LOCATION_BOTTOM_RIGHT = tk.SE

THEME_DEFAULT = 'default'
THEME_WINNATIVE = 'winnative'
THEME_CLAM = 'clam'
THEME_ALT = 'alt'
THEME_CLASSIC = 'classic'
THEME_VISTA = 'vista'
THEME_XPNATIVE = 'xpnative'

# DEFAULT_METER_ORIENTATION = 'Vertical'
# ----====----====----==== Constants the user should NOT f-with ====----====----====----#
ThisRow = 555666777  # magic number

# DEFAULT_WINDOW_ICON = ''
MESSAGE_BOX_LINE_WIDTH = 60

# "Special" Key Values.. reserved
# Key representing a Read timeout
TIMEOUT_KEY = '__TIMEOUT__'
# Key indicating should not create any return values for element
WRITE_ONLY_KEY = '__WRITE ONLY__'

MENU_DISABLED_CHARACTER = '!'
MENU_KEY_SEPARATOR = '::'


# ====================================================================== #
# One-liner functions that are handy as f_ck                             #
# ====================================================================== #
def RGB(red, green, blue): return '#%02x%02x%02x' % (red, green, blue)


# ====================================================================== #
# Enums for types                                                        #
# ====================================================================== #
# -------------------------  Button types  ------------------------- #
# todo Consider removing the Submit, Cancel types... they are just 'RETURN' type in reality
# uncomment this line and indent to go back to using Enums
BUTTON_TYPE_BROWSE_FOLDER = 1
BUTTON_TYPE_BROWSE_FILE = 2
BUTTON_TYPE_BROWSE_FILES = 21
BUTTON_TYPE_SAVEAS_FILE = 3
BUTTON_TYPE_CLOSES_WIN = 5
BUTTON_TYPE_CLOSES_WIN_ONLY = 6
BUTTON_TYPE_READ_FORM = 7
BUTTON_TYPE_REALTIME = 9
BUTTON_TYPE_CALENDAR_CHOOSER = 30
BUTTON_TYPE_COLOR_CHOOSER = 40
BUTTON_TYPE_SHOW_DEBUGGER = 50

# -------------------------  Element types  ------------------------- #

ELEM_TYPE_TEXT = 'text'
ELEM_TYPE_INPUT_TEXT = 'input'
ELEM_TYPE_INPUT_COMBO = 'combo'
ELEM_TYPE_INPUT_OPTION_MENU = 'option menu'
ELEM_TYPE_INPUT_RADIO = 'radio'
ELEM_TYPE_INPUT_MULTILINE = 'multiline'
ELEM_TYPE_INPUT_CHECKBOX = 'checkbox'
ELEM_TYPE_INPUT_SPIN = 'spind'
ELEM_TYPE_BUTTON = 'button'
ELEM_TYPE_IMAGE = 'image'
ELEM_TYPE_CANVAS = 'canvas'
ELEM_TYPE_FRAME = 'frame'
ELEM_TYPE_GRAPH = 'graph'
ELEM_TYPE_TAB = 'tab'
ELEM_TYPE_TAB_GROUP = 'tabgroup'
ELEM_TYPE_INPUT_SLIDER = 'slider'
ELEM_TYPE_INPUT_LISTBOX = 'listbox'
ELEM_TYPE_OUTPUT = 'output'
ELEM_TYPE_COLUMN = 'column'
ELEM_TYPE_MENUBAR = 'menubar'
ELEM_TYPE_PROGRESS_BAR = 'progressbar'
ELEM_TYPE_BLANK = 'blank'
ELEM_TYPE_TABLE = 'table'
ELEM_TYPE_TREE = 'tree'
ELEM_TYPE_ERROR = 'error'
ELEM_TYPE_SEPARATOR = 'separator'
ELEM_TYPE_STATUSBAR = 'statusbar'
ELEM_TYPE_PANE = 'pane'
ELEM_TYPE_BUTTONMENU = 'buttonmenu'

# STRETCH == ERROR ELEMENT as a filler

# -------------------------  Popup Buttons Types  ------------------------- #
POPUP_BUTTONS_YES_NO = 1
POPUP_BUTTONS_CANCELLED = 2
POPUP_BUTTONS_ERROR = 3
POPUP_BUTTONS_OK_CANCEL = 4
POPUP_BUTTONS_OK = 0
POPUP_BUTTONS_NO_BUTTONS = 5


# ------------------------------------------------------------------------- #
#                       ToolTip used by the Elements                        #
# ------------------------------------------------------------------------- #

class ToolTip:
    """Create a tooltip for a given widget
    (inspired by https://stackoverflow.com/a/36221216)
    """
    def __init__(self, widget, text, timeout=DEFAULT_TOOLTIP_TIME):
        """

        :param widget: 
        :param text: 
        :param timeout:  (Default value = DEFAULT_TOOLTIP_TIME)

        """
        self.widget = widget
        self.text = text
        self.timeout = timeout
        # self.wraplength = wraplength if wraplength else widget.winfo_screenwidth() // 2
        self.tipwindow = None
        self.id = None
        self.x = self.y = 0
        self.widget.bind("<Enter>", self.enter)
        self.widget.bind("<Leave>", self.leave)
        self.widget.bind("<ButtonPress>", self.leave)

    def enter(self, event=None):
        """

        :param event:  (Default value = None)

        """
        self.x = event.x
        self.y = event.y
        self.schedule()

    def leave(self, event=None):
        """

        :param event:  (Default value = None)

        """
        self.unschedule()
        self.hidetip()

    def schedule(self):
        """ """
        self.unschedule()
        self.id = self.widget.after(self.timeout, self.showtip)

    def unschedule(self):
        """ """
        if self.id:
            self.widget.after_cancel(self.id)
        self.id = None

    def showtip(self):
        """ """
        if self.tipwindow:
            return
        x = self.widget.winfo_rootx() + self.x + DEFAULT_TOOLTIP_OFFSET[0]
        y = self.widget.winfo_rooty() + self.y + DEFAULT_TOOLTIP_OFFSET[1]
        self.tipwindow = tk.Toplevel(self.widget)
        self.tipwindow.wm_overrideredirect(True)
        self.tipwindow.wm_geometry("+%d+%d" % (x, y))
        self.tipwindow.wm_attributes("-topmost", 1)

        label = ttk.Label(self.tipwindow, text=self.text, justify=tk.LEFT,
                          background="#ffffe0", relief=tk.SOLID, borderwidth=1)
        label.pack()

    def hidetip(self):
        """ """
        if self.tipwindow:
            self.tipwindow.destroy()
        self.tipwindow = None


# ---------------------------------------------------------------------- #
# Cascading structure.... Objects get larger                             #
#   Button                                                               #
#       Element                                                          #
#           Row                                                          #
#               Form                                                     #
# ---------------------------------------------------------------------- #
# ------------------------------------------------------------------------- #
#                       Element CLASS                                       #
# ------------------------------------------------------------------------- #
class Element():
    """The base class for all Elements.
    Holds the basic description of an Element like size and colors


    """
    def __init__(self, type, size=(None, None), auto_size_text=None, font=None, background_color=None, text_color=None, key=None, pad=None, tooltip=None, visible=True):
        """

        :param type: 
        :param size: (common_key) (w,h) w=characters-wide, h=rows-high (Default value = (None, None))
        :param auto_size_text: True if size should fit the text length (Default value = None)
        :param font: (common_key) specifies the font family, size, etc (Default value = None)
        :param background_color: color of background (Default value = None)
        :param text_color: element's text color (Default value = None)
        :param key: (common_key) Used with window.FindElement and with return values (Default value = None)
        :param pad: (common_key) Amount of padding to put around element (Default value = None)
        :param tooltip: text, that will appear the you hover on (Default value = None)
        :param visible: set visibility state of the element (Default value = True)

        """
        self.Size = size
        self.Type = type
        self.AutoSizeText = auto_size_text
        self.Pad = pad
        self.Font = font

        self.TKStringVar = None
        self.TKIntVar = None
        self.TKText = None
        self.TKEntry = None
        self.TKImage = None

        self.ParentForm = None  # type: Window
        self.ParentContainer = None  # will be a Form, Column, or Frame element
        self.TextInputDefault = None
        self.Position = (0, 0)  # Default position Row 0, Col 0
        self.BackgroundColor = background_color if background_color is not None else DEFAULT_ELEMENT_BACKGROUND_COLOR
        self.TextColor = text_color if text_color is not None else DEFAULT_ELEMENT_TEXT_COLOR
        self.Key = key  # dictionary key for return values
        self.Tooltip = tooltip
        self.TooltipObject = None
        self.Visible = visible
        self.TKRightClickMenu = None
        self.Widget = None  # Set when creating window. Has the main tkinter widget for element

    def _RightClickMenuCallback(self, event):
        """

        :param event: 

        """
        self.TKRightClickMenu.tk_popup(event.x_root, event.y_root, 0)
        self.TKRightClickMenu.grab_release()

    def _MenuItemChosenCallback(self, item_chosen):  # TEXT Menu item callback
        """

        :param item_chosen: 

        """
        # print('IN MENU ITEM CALLBACK', item_chosen)
        self.MenuItemChosen = item_chosen.replace('&', '')
        self.ParentForm.LastButtonClicked = self.MenuItemChosen
        self.ParentForm.FormRemainedOpen = True
        if self.ParentForm.CurrentlyRunningMainloop:
            self.ParentForm.TKroot.quit()  # kick the users out of the mainloop

    def _FindReturnKeyBoundButton(self, form):
        """

        :param form: 

        """
        for row in form.Rows:
            for element in row:
                if element.Type == ELEM_TYPE_BUTTON:
                    if element.BindReturnKey:
                        return element
                if element.Type == ELEM_TYPE_COLUMN:
                    rc = self._FindReturnKeyBoundButton(element)
                    if rc is not None:
                        return rc
                if element.Type == ELEM_TYPE_FRAME:
                    rc = self._FindReturnKeyBoundButton(element)
                    if rc is not None:
                        return rc
                if element.Type == ELEM_TYPE_TAB_GROUP:
                    rc = self._FindReturnKeyBoundButton(element)
                    if rc is not None:
                        return rc
                if element.Type == ELEM_TYPE_TAB:
                    rc = self._FindReturnKeyBoundButton(element)
                    if rc is not None:
                        return rc
                if element.Type == ELEM_TYPE_PANE:
                    rc = self._FindReturnKeyBoundButton(element)
                    if rc is not None:
                        return rc
        return None

    def _TextClickedHandler(self, event):
        """

        :param event: 

        """
        if self.Key is not None:
            self.ParentForm.LastButtonClicked = self.Key
        else:
            self.ParentForm.LastButtonClicked = self.DisplayText
        self.ParentForm.FormRemainedOpen = True
        if self.ParentForm.CurrentlyRunningMainloop:
            self.ParentForm.TKroot.quit()  # kick the users out of the mainloop

    def _ReturnKeyHandler(self, event):
        """

        :param event: 

        """
        MyForm = self.ParentForm
        button_element = self._FindReturnKeyBoundButton(MyForm)
        if button_element is not None:
            button_element.ButtonCallBack()

    def _ListboxSelectHandler(self, event):
        """

        :param event: 

        """
        # first, get the results table built
        # modify the Results table in the parent FlexForm object
        if self.Key is not None:
            self.ParentForm.LastButtonClicked = self.Key
        else:
            self.ParentForm.LastButtonClicked = ''
        self.ParentForm.FormRemainedOpen = True
        if self.ParentForm.CurrentlyRunningMainloop:
            self.ParentForm.TKroot.quit()  # kick the users out of the mainloop

    def _ComboboxSelectHandler(self, event):
        """

        :param event: 

        """
        # first, get the results table built
        # modify the Results table in the parent FlexForm object
        if self.Key is not None:
            self.ParentForm.LastButtonClicked = self.Key
        else:
            self.ParentForm.LastButtonClicked = ''
        self.ParentForm.FormRemainedOpen = True
        if self.ParentForm.CurrentlyRunningMainloop:
            self.ParentForm.TKroot.quit()  # kick the users out of the mainloop

    def _RadioHandler(self):
        """ """
        if self.Key is not None:
            self.ParentForm.LastButtonClicked = self.Key
        else:
            self.ParentForm.LastButtonClicked = ''
        self.ParentForm.FormRemainedOpen = True
        if self.ParentForm.CurrentlyRunningMainloop:
            self.ParentForm.TKroot.quit()

    def _CheckboxHandler(self):
        """ """
        if self.Key is not None:
            self.ParentForm.LastButtonClicked = self.Key
        else:
            self.ParentForm.LastButtonClicked = ''
        self.ParentForm.FormRemainedOpen = True
        if self.ParentForm.CurrentlyRunningMainloop:
            self.ParentForm.TKroot.quit()

    def _TabGroupSelectHandler(self, event):
        """

        :param event: 

        """
        if self.Key is not None:
            self.ParentForm.LastButtonClicked = self.Key
        else:
            self.ParentForm.LastButtonClicked = ''
        self.ParentForm.FormRemainedOpen = True
        if self.ParentForm.CurrentlyRunningMainloop:
            self.ParentForm.TKroot.quit()

    def _KeyboardHandler(self, event):
        """

        :param event: 

        """
        if self.Key is not None:
            self.ParentForm.LastButtonClicked = self.Key
        else:
            self.ParentForm.LastButtonClicked = ''
        self.ParentForm.FormRemainedOpen = True
        if self.ParentForm.CurrentlyRunningMainloop:
            self.ParentForm.TKroot.quit()

    def _ClickHandler(self, event):
        """

        :param event: 

        """
        if self.Key is not None:
            self.ParentForm.LastButtonClicked = self.Key
        else:
            self.ParentForm.LastButtonClicked = ''
        self.ParentForm.FormRemainedOpen = True
        if self.ParentForm.CurrentlyRunningMainloop:
            self.ParentForm.TKroot.quit()

    def SetTooltip(self, tooltip_text):
        """

        :param tooltip_text: 

        """
        self.TooltipObject = ToolTip(self.Widget, text=tooltip_text, timeout=DEFAULT_TOOLTIP_TIME)

    def __del__(self):
        """ """
        try:
            self.TKStringVar.__del__()
        except:
            pass
        try:
            self.TKIntVar.__del__()
        except:
            pass
        try:
            self.TKText.__del__()
        except:
            pass
        try:
            self.TKEntry.__del__()
        except:
            pass


# ---------------------------------------------------------------------- #
#                           Input Class                                  #
# ---------------------------------------------------------------------- #
class InputText(Element):
    """Shows a single line of input."""
    def __init__(self, default_text='', size=(None, None), disabled=False, password_char='',
                 justification=None, background_color=None,   text_color=None, font=None, tooltip=None,
                 change_submits=False, enable_events=False, do_not_clear=True, key=None, focus=False, pad=None,
                 right_click_menu=None, visible=True):
        """

        :param default_text:  (Default value = '')
        :param size: (common_key) (w,h) w=characters-wide, h=rows-high (Default value = (None, None))
        :param disabled: set disable state for element (Default value = False)
        :param password_char: Passwork character if this is a password field (Default value = '')
        :param justification: justification for data display (Default value = None)
        :param background_color: color of background (Default value = None)
        :param text_color: color of the text (Default value = None)
        :param font: (common_key) specifies the font family, size, etc (Default value = None)
        :param tooltip: text, that will appear the you hover on (Default value = None)
        :param change_submits: If True, pressing Enter key submits window- DEPRICATED DO NOT USE! (Default value = False)
        :param enable_events: Turns on the element specific events. Use this instead of change_submits (Default value = False)
        :param do_not_clear: see docx (Default value = True)
        :param key: (common_key) Used with window.FindElement and with return values (Default value = None)
        :param focus: if focus should be set to this (Default value = None)
        :param pad: (common_key) Amount of padding to put around element (Default value = None)
        :param right_click_menu: see "Right Click Menus" (Default value = None)
        :param visible: set visibility state of the element (Default value = True)
        """
        self.DefaultText = default_text
        self.PasswordCharacter = password_char
        bg = background_color if background_color is not None else DEFAULT_INPUT_ELEMENTS_COLOR
        fg = text_color if text_color is not None else DEFAULT_INPUT_TEXT_COLOR
        self.Focus = focus
        self.do_not_clear = do_not_clear
        self.Justification = justification
        self.Disabled = disabled
        self.ChangeSubmits = change_submits or enable_events
        self.RightClickMenu = right_click_menu
        self.TKEntry = self.Widget = None          # type: tk.Entry
        super().__init__(ELEM_TYPE_INPUT_TEXT, size=size, background_color=bg, text_color=fg, key=key, pad=pad,
                         font=font, tooltip=tooltip, visible=visible)

    def Update(self, value=None, disabled=None, select=None, visible=None):
        """

        :param value:  (Default value = None)
        :param disabled: disable or enable state of the element (Default value = None)
        :param select:  (Default value = None)
        :param visible:  change visibility of element (Default value = None)

        """
        #NOTE - Read or Finalize must be called on Window prior to Update call
        if disabled is True:
            self.TKEntry['state'] = 'readonly'
        elif disabled is False:
            self.TKEntry['state'] = 'normal'
        if value is not None:
            try:
                self.TKStringVar.set(value)
            except:
                pass
            self.DefaultText = value
        if select:
            self.TKEntry.select_range(0, 'end')
        if visible is False:
            self.TKEntry.pack_forget()
        elif visible is True:
            self.TKEntry.pack()

    def Get(self):
        """ """
        try:
            text = self.TKStringVar.get()
        except:
            text = ''
        return text

    def SetFocus(self):
        """ """
        try:
            self.TKEntry.focus_set()
        except:
            pass

    def __del__(self):
        """ """
        super().__del__()


# -------------------------  INPUT TEXT Element lazy functions  ------------------------- #
In = InputText
Input = InputText
I = InputText


# ---------------------------------------------------------------------- #
#                           Combo                                        #
# ---------------------------------------------------------------------- #
class Combo(Element):
    """ComboBox Element"""
    def __init__(self, values, default_value=None, size=(None, None), auto_size_text=None, background_color=None,
                 text_color=None, change_submits=False, enable_events=False, disabled=False, key=None, pad=None,
                 tooltip=None, readonly=False, font=None, visible=True):
        """Combo Element - Combo Box, Drop Down Menu, ...

        :param values: 
        :param default_value:  (Default value = None)
        :param size: (common_key) (w,h) w=characters-wide, h=rows-high (Default value = (None, None))
        :param auto_size_text: True if size should fit the text length (Default value = None)
        :param background_color: color of background (Default value = None)
        :param text_color: color of the text (Default value = None)
        :param change_submits: If True, pressing Enter key submits window (Default value = False)
        :param enable_events: Turns on the element specific events.(Default value = False)
        :param disabled: set disable state for element (Default value = False)
        :param key: (common_key) Used with window.FindElement and with return values (Default value = None)
        :param pad: (common_key) Amount of padding to put around element (Default value = None)
        :param tooltip: text, that will appear the you hover on (Default value = None)
        :param readonly:  make element readonly (Default value = False)
        :param font: (common_key) specifies the font family, size, etc (Default value = None)
        :param visible: set visibility state of the element (Default value = True)

        """
        self.Values = values
        self.DefaultValue = default_value
        self.ChangeSubmits = change_submits or enable_events
        self.TKCombo = None
        # self.InitializeAsDisabled = disabled
        self.Disabled = disabled
        self.Readonly = readonly
        bg = background_color if background_color else DEFAULT_INPUT_ELEMENTS_COLOR
        fg = text_color if text_color is not None else DEFAULT_INPUT_TEXT_COLOR

        super().__init__(ELEM_TYPE_INPUT_COMBO, size=size, auto_size_text=auto_size_text, background_color=bg,
                         text_color=fg, key=key, pad=pad, tooltip=tooltip, font=font or DEFAULT_FONT, visible=visible)

    def Update(self, value=None, values=None, set_to_index=None, disabled=None, readonly=None, font=None, visible=None):
        """
        :param value:  (Default value = None)
        :param values:  (Default value = None)
        :param set_to_index:  (Default value = None)
        :param disabled: disable or enable state of the element (Default value = None)
        :param readonly:  make element readonly (Default value = None)
        :param font: (common_key) specifies the font family, size, etc (Default value = None)
        :param visible:  change visibility of element (Default value = None)

        """
        if values is not None:
            try:
                self.TKCombo['values'] = values
                self.TKCombo.current(0)
            except:
                pass
            self.Values = values
        if value is not None:
            for index, v in enumerate(self.Values):
                if v == value:
                    try:
                        self.TKCombo.current(index)
                    except:
                        pass
                    self.DefaultValue = value
                    break
        if set_to_index is not None:
            try:
                self.TKCombo.current(set_to_index)
                self.DefaultValue = self.Values[set_to_index]
            except:
                pass
        if disabled == True:
            self.TKCombo['state'] = 'disable'
        elif disabled == False:
            self.TKCombo['state'] = 'enable'
            if readonly is not None:
                self.Readonly = readonly
            if self.Readonly:
                self.TKCombo['state'] = 'readonly'
        if font is not None:
            self.TKCombo.configure(font=font)
        if visible is False:
            self.TKCombo.pack_forget()
        elif visible is True:
            self.TKCombo.pack()

    def __del__(self):
        """ """
        try:
            self.TKCombo.__del__()
        except:
            pass
        super().__del__()


# -------------------------  INPUT COMBO Element lazy functions  ------------------------- #
InputCombo = Combo
DropDown = InputCombo
Drop = InputCombo


# ---------------------------------------------------------------------- #
#                           Option Menu                                  #
# ---------------------------------------------------------------------- #
class OptionMenu(Element):
    """Option Menu is an Element available ONLY on the tkinter port of PySimpleGUI.  It's is a widget that is unique
    to tkinter.  However, it looks much like a ComboBox.  Instead of an arrow to click to pull down the list of
    choices, another little graphic is shown on the widget to indicate where you click.  After clicking to activate,
    it looks like a Combo Box that you scroll to select a choice.


    """
    def __init__(self, values, default_value=None, size=(None, None), disabled=False, auto_size_text=None,
                 background_color=None, text_color=None, key=None, pad=None, tooltip=None, visible=True):
        """Option Menu Element

        :param values: 
        :param default_value:  (Default value = None)
        :param size: (common_key) (w,h) w=characters-wide, h=rows-high (Default value = (None, None))
        :param disabled: set disable state for element (Default value = False)
        :param auto_size_text: True if size should fit the text length (Default value = None)
        :param background_color: color of background (Default value = None)
        :param text_color: color of the text (Default value = None)
        :param key: (common_key) Used with window.FindElement and with return values (Default value = None)
        :param pad: (common_key) Amount of padding to put around element (Default value = None)
        :param tooltip: text, that will appear the you hover on (Default value = None)
        :param visible: set visibility state of the element (Default value = True)

        """
        self.Values = values
        self.DefaultValue = default_value
        self.TKOptionMenu = None  # type: tk.OptionMenu
        self.Disabled = disabled
        bg = background_color if background_color else DEFAULT_INPUT_ELEMENTS_COLOR
        fg = text_color if text_color is not None else DEFAULT_INPUT_TEXT_COLOR

        super().__init__(ELEM_TYPE_INPUT_OPTION_MENU, size=size, auto_size_text=auto_size_text, background_color=bg,
                         text_color=fg, key=key, pad=pad, tooltip=tooltip, visible=visible)

    def Update(self, value=None, values=None, disabled=None, visible=None):
        """OptionMenu Element Update

        :param value:  (Default value = None)
        :param values:  (Default value = None)
        :param disabled: disable or enable state of the element (Default value = None)
        :param visible:  change visibility of element (Default value = None)

        """
        if values is not None:
            self.Values = values
            self.TKOptionMenu['menu'].delete(0, 'end')

            # Insert list of new options (tk._setit hooks them up to var)
            self.TKStringVar.set(self.Values[0])
            for new_value in self.Values:
                self.TKOptionMenu['menu'].add_command(label=new_value, command=tk._setit(self.TKStringVar, new_value))

        if self.Values is not None:
            for index, v in enumerate(self.Values):
                if v == value:
                    try:
                        self.TKStringVar.set(value)
                    except:
                        pass
                    self.DefaultValue = value
                    break
        if disabled == True:
            self.TKOptionMenu['state'] = 'disabled'
        elif disabled == False:
            self.TKOptionMenu['state'] = 'normal'
        if visible is False:
            self.TKOptionMenu.pack_forget()
        elif visible is True:
            self.TKOptionMenu.pack()

    def __del__(self):
        """ """
        try:
            self.TKOptionMenu.__del__()
        except:
            pass
        super().__del__()


# -------------------------  OPTION MENU Element lazy functions  ------------------------- #
InputOptionMenu = OptionMenu


# ---------------------------------------------------------------------- #
#                           Listbox                                      #
# ---------------------------------------------------------------------- #
class Listbox(Element):
    """A List Box.  Provide a list of values for the user to choose one or more of.   Returns a list of selected rows
    when a window.Read() is executed.


    """
    def __init__(self, values, default_values=None, select_mode=None, change_submits=False, enable_events=False,
                 bind_return_key=False, size=(None, None), disabled=False, auto_size_text=None, font=None,
                 background_color=None, text_color=None, key=None, pad=None, tooltip=None, right_click_menu=None,
                 visible=True):
        """Listbox Element

        :param values: 
        :param default_values:  (Default value = None)
        :param select_mode:  (Default value = None)
        :param change_submits: If True, pressing Enter key submits window (Default value = False)
        :param enable_events: Turns on the element specific events.(Default value = False)
        :param bind_return_key:  (Default value = False)
        :param size: (common_key) (w,h) w=characters-wide, h=rows-high (Default value = (None, None))
        :param disabled: set disable state for element (Default value = False)
        :param auto_size_text: True if size should fit the text length (Default value = None)
        :param font: (common_key) specifies the font family, size, etc (Default value = None)
        :param background_color: color of background (Default value = None)
        :param text_color: color of the text (Default value = None)
        :param key: (common_key) Used with window.FindElement and with return values (Default value = None)
        :param pad: (common_key) Amount of padding to put around element (Default value = None)
        :param tooltip: text, that will appear the you hover on (Default value = None)
        :param right_click_menu: see "Right Click Menus" (Default value = None)
        :param visible: set visibility state of the element (Default value = True)

        """
        self.Values = values
        self.DefaultValues = default_values
        self.TKListbox = None
        self.ChangeSubmits = change_submits or enable_events
        self.BindReturnKey = bind_return_key
        self.Disabled = disabled
        if select_mode == LISTBOX_SELECT_MODE_BROWSE:
            self.SelectMode = SELECT_MODE_BROWSE
        elif select_mode == LISTBOX_SELECT_MODE_EXTENDED:
            self.SelectMode = SELECT_MODE_EXTENDED
        elif select_mode == LISTBOX_SELECT_MODE_MULTIPLE:
            self.SelectMode = SELECT_MODE_MULTIPLE
        elif select_mode == LISTBOX_SELECT_MODE_SINGLE:
            self.SelectMode = SELECT_MODE_SINGLE
        else:
            self.SelectMode = DEFAULT_LISTBOX_SELECT_MODE
        bg = background_color if background_color else DEFAULT_INPUT_ELEMENTS_COLOR
        fg = text_color if text_color is not None else DEFAULT_INPUT_TEXT_COLOR
        self.RightClickMenu = right_click_menu
        self.vsb = None  # type: tk.Scrollbar
        self.TKListbox = self.Widget = None         # type: tk.Listbox
        super().__init__(ELEM_TYPE_INPUT_LISTBOX, size=size, auto_size_text=auto_size_text, font=font,
                         background_color=bg, text_color=fg, key=key, pad=pad, tooltip=tooltip, visible=visible)

    def Update(self, values=None, disabled=None, set_to_index=None, visible=None):
        """

        :param values:  (Default value = None)
        :param disabled: disable or enable state of the element (Default value = None)
        :param set_to_index:  (Default value = None)
        :param visible:  change visibility of element (Default value = None)

        """
        
        if disabled == True:
            self.TKListbox.configure(state='disabled')
        elif disabled == False:
            self.TKListbox.configure(state='normal')
        if values is not None:
            self.TKListbox.delete(0, 'end')
            for item in values:
                self.TKListbox.insert(tk.END, item)
            self.TKListbox.selection_set(0, 0)
            self.Values = values
        if set_to_index is not None:
            self.TKListbox.selection_clear(0)
            try:
                self.TKListbox.selection_set(set_to_index, set_to_index)
            except:
                pass
        if visible is False:
            self.TKListbox.pack_forget()
            self.vsb.pack_forget()
        elif visible is True:
            self.TKListbox.pack()
            self.vsb.pack()

    def SetValue(self, values):
        """

        :param values: 

        """
        for index, item in enumerate(self.Values):
            try:
                if item in values:
                    self.TKListbox.selection_set(index)
                else:
                    self.TKListbox.selection_clear(index)
            except:
                pass
        self.DefaultValues = values

    def GetListValues(self):
        """ """
        return self.Values

    def SetFocus(self):
        """ """
        try:
            self.TKListbox.focus_set()
        except:
            pass

    def __del__(self):
        """ """
        try:
            self.TKListBox.__del__()
        except:
            pass
        super().__del__()


# ---------------------------------------------------------------------- #
#                           Radio                                        #
# ---------------------------------------------------------------------- #
class Radio(Element):
    """Radio Button Element - Used in a group of other Radio Elements to provide user with ability to select only
    1 choice in a list of choices.


    """
    def __init__(self, text, group_id, default=False, disabled=False, size=(None, None), auto_size_text=None,
                 background_color=None, text_color=None, font=None, key=None, pad=None, tooltip=None,
                 change_submits=False, enable_events=False, visible=True):
        """

        :param text: 
        :param group_id: 
        :param default:  (Default value = False)
        :param disabled: set disable state for element (Default value = False)
        :param size: (common_key) (w,h) w=characters-wide, h=rows-high (Default value = (None, None))
        :param auto_size_text: True if size should fit the text length (Default value = None)
        :param background_color: color of background (Default value = None)
        :param text_color: color of the text (Default value = None)
        :param font: (common_key) specifies the font family, size, etc (Default value = None)
        :param key: (common_key) Used with window.FindElement and with return values (Default value = None)
        :param pad: (common_key) Amount of padding to put around element (Default value = None)
        :param tooltip: text, that will appear the you hover on (Default value = None)
        :param change_submits: If True, pressing Enter key submits window (Default value = False)
        :param enable_events: Turns on the element specific events.(Default value = False)
        :param visible: set visibility state of the element (Default value = True)

        """
        
        self.InitialState = default
        self.Text = text
        self.TKRadio = None
        self.GroupID = group_id
        self.Value = None
        self.Disabled = disabled
        self.TextColor = text_color or DEFAULT_TEXT_COLOR
        self.ChangeSubmits = change_submits or enable_events
        self.EncodedRadioValue = None
        super().__init__(ELEM_TYPE_INPUT_RADIO, size=size, auto_size_text=auto_size_text, font=font,
                         background_color=background_color, text_color=self.TextColor, key=key, pad=pad,
                         tooltip=tooltip, visible=visible)

    def Update(self, value=None, disabled=None, visible=None):
        """

        :param value:  (Default value = None)
        :param disabled: disable or enable state of the element (Default value = None)
        :param visible:  change visibility of element (Default value = None)

        """
        
        if value is not None:
            try:
                self.TKIntVar.set(self.EncodedRadioValue)
            except:
                pass
            self.InitialState = value
        if disabled == True:
            self.TKRadio['state'] = 'disabled'
        elif disabled == False:
            self.TKRadio['state'] = 'normal'
        if visible is False:
            self.TKRadio.pack_forget()
        elif visible is True:
            self.TKRadio.pack()

    def ResetGroup(self):
        """ """
        self.TKIntVar.set(0)

    def __del__(self):
        """ """
        try:
            self.TKRadio.__del__()
        except:
            pass
        super().__del__()


# ---------------------------------------------------------------------- #
#                           Checkbox                                     #
# ---------------------------------------------------------------------- #
##########################################################################
# June 15, 2019 - This is the last element that has been converted to use the new
# Doc strings
# Note - The renaming of the member function to have _ if internal only has NOT yet been done!
class Checkbox(Element):
    """ """
    
    def __init__(self, text, default=False, size=(None, None), auto_size_text=None, font=None, background_color=None,
                 text_color=None, change_submits=False, enable_events=False, disabled=False, key=None, pad=None,
                 tooltip=None, visible=True):
        """

        :param text: 
        :param default:  (Default value = False)
        :param size: (common_key) (w,h) w=characters-wide, h=rows-high (Default value = (None, None))
        :param auto_size_text: True if size should fit the text length (Default value = None)
        :param font: (common_key) specifies the font family, size, etc (Default value = None)
        :param background_color: color of background (Default value = None)
        :param text_color: color of the text (Default value = None)
        :param change_submits: If True, pressing Enter key submits window (Default value = False)
        :param enable_events: Turns on the element specific events.(Default value = False)
        :param disabled: set disable state for element (Default value = False)
        :param key: (common_key) Used with window.FindElement and with return values (Default value = None)
        :param pad: (common_key) Amount of padding to put around element (Default value = None)
        :param tooltip: text, that will appear the you hover on (Default value = None)
        :param visible: set visibility state of the element (Default value = True)

        """
        
        self.Text = text
        self.InitialState = default
        self.Value = None
        self.TKCheckbutton = None
        self.Disabled = disabled
        self.TextColor = text_color if text_color else DEFAULT_TEXT_COLOR
        self.ChangeSubmits = change_submits or enable_events

        super().__init__(ELEM_TYPE_INPUT_CHECKBOX, size=size, auto_size_text=auto_size_text, font=font,
                         background_color=background_color, text_color=self.TextColor, key=key, pad=pad,
                         tooltip=tooltip, visible=visible)

    def Get(self):
        """ """
        return self.TKIntVar.get()

    def Update(self, value=None, disabled=None, visible=None):
        """

        :param value:  (Default value = None)
        :param disabled: disable or enable state of the element (Default value = None)
        :param visible:  change visibility of element (Default value = None)

        """
        
        if value is not None:
            try:
                self.TKIntVar.set(value)
                self.InitialState = value
            except:
                print('Checkbox update failed')
        if disabled == True:
            self.TKCheckbutton.configure(state='disabled')
        elif disabled == False:
            self.TKCheckbutton.configure(state='normal')
        if visible is False:
            self.TKCheckbutton.pack_forget()
        elif visible is True:
            self.TKCheckbutton.pack()

    def __del__(self):
        """ """
        super().__del__()


# -------------------------  CHECKBOX Element lazy functions  ------------------------- #
CB = Checkbox
CBox = Checkbox
Check = Checkbox


# ---------------------------------------------------------------------- #
#                           Spin                                         #
# ---------------------------------------------------------------------- #

class Spin(Element):
    """ """
    
    def __init__(self, values, initial_value=None, disabled=False, change_submits=False, enable_events=False,
                 size=(None, None), auto_size_text=None, font=None, background_color=None, text_color=None, key=None,
                 pad=None, tooltip=None, visible=True):
        """

        :param values: 
        :param initial_value:  (Default value = None)
        :param disabled: set disable state for element (Default value = False)
        :param change_submits: If True, pressing Enter key submits window (Default value = False)
        :param enable_events: Turns on the element specific events.(Default value = False)
        :param size: (common_key) (w,h) w=characters-wide, h=rows-high (Default value = (None, None))
        :param auto_size_text: True if size should fit the text length (Default value = None)
        :param font: (common_key) specifies the font family, size, etc (Default value = None)
        :param background_color: color of background (Default value = None)
        :param text_color: color of the text (Default value = None)
        :param key: (common_key) Used with window.FindElement and with return values (Default value = None)
        :param pad: (common_key) Amount of padding to put around element (Default value = None)
        :param tooltip: text, that will appear the you hover on (Default value = None)
        :param visible: set visibility state of the element (Default value = True)

        """
        
        self.Values = values
        self.DefaultValue = initial_value
        self.ChangeSubmits = change_submits or enable_events
        self.TKSpinBox = None
        self.Disabled = disabled
        bg = background_color if background_color else DEFAULT_INPUT_ELEMENTS_COLOR
        fg = text_color if text_color is not None else DEFAULT_INPUT_TEXT_COLOR

        super().__init__(ELEM_TYPE_INPUT_SPIN, size, auto_size_text, font=font, background_color=bg, text_color=fg,
                         key=key, pad=pad, tooltip=tooltip, visible=visible)
        return

    def Update(self, value=None, values=None, disabled=None, visible=None):
        """

        :param value:  (Default value = None)
        :param values:  (Default value = None)
        :param disabled: disable or enable state of the element (Default value = None)
        :param visible:  change visibility of element (Default value = None)

        """
        
        if values != None:
            old_value = self.TKStringVar.get()
            self.Values = values
            self.TKSpinBox.configure(values=values)
            self.TKStringVar.set(old_value)
        if value is not None:
            try:
                self.TKStringVar.set(value)
            except:
                pass
        self.DefaultValue = value
        if disabled == True:
            self.TKSpinBox.configure(state='disabled')
        elif disabled == False:
            self.TKSpinBox.configure(state='normal')
        if visible is False:
            self.TKSpinBox.pack_forget()
        elif visible is True:
            self.TKSpinBox.pack()

    def SpinChangedHandler(self, event):
        """

        :param event: 

        """
        # first, get the results table built
        # modify the Results table in the parent FlexForm object
        if self.Key is not None:
            self.ParentForm.LastButtonClicked = self.Key
        else:
            self.ParentForm.LastButtonClicked = ''
        self.ParentForm.FormRemainedOpen = True
        if self.ParentForm.CurrentlyRunningMainloop:
            self.ParentForm.TKroot.quit()  # kick the users out of the mainloop

    def Get(self):
        """ """
        return self.TKStringVar.get()

    def __del__(self):
        """ """
        try:
            self.TKSpinBox.__del__()
        except:
            pass
        super().__del__()


# ---------------------------------------------------------------------- #
#                           Multiline                                    #
# ---------------------------------------------------------------------- #
class Multiline(Element):
    """ """
    
    def __init__(self, default_text='', enter_submits=False, disabled=False, autoscroll=False, border_width=None,
                 size=(None, None), auto_size_text=None, background_color=None, text_color=None, change_submits=False,
                 enable_events=False, do_not_clear=True, key=None, focus=False, font=None, pad=None, tooltip=None,
                 right_click_menu=None, visible=True):
        """

        :param default_text:  (Default value = '')
        :param enter_submits:  (Default value = False)
        :param disabled: set disable state for element (Default value = False)
        :param autoscroll:  (Default value = False)
        :param border_width:  (Default value = None)
        :param size: (common_key) (w,h) w=characters-wide, h=rows-high (Default value = (None, None))
        :param auto_size_text: True if size should fit the text length (Default value = None)
        :param background_color: color of background (Default value = None)
        :param text_color: color of the text (Default value = None)
        :param change_submits: If True, pressing Enter key submits window (Default value = False)
        :param enable_events: Turns on the element specific events.(Default value = False)
        :param do_not_clear: see docx (Default value = True)
        :param key: (common_key) Used with window.FindElement and with return values (Default value = None)
        :param focus: if focus should be set to this (Default value = None)
        :param font: (common_key) specifies the font family, size, etc (Default value = None)
        :param pad: (common_key) Amount of padding to put around element (Default value = None)
        :param tooltip: text, that will appear the you hover on (Default value = None)
        :param right_click_menu: see "Right Click Menus" (Default value = None)
        :param visible: set visibility state of the element (Default value = True)

        """
        

        self.DefaultText = default_text
        self.EnterSubmits = enter_submits
        bg = background_color if background_color else DEFAULT_INPUT_ELEMENTS_COLOR
        self.Focus = focus
        self.do_not_clear = do_not_clear
        fg = text_color if text_color is not None else DEFAULT_INPUT_TEXT_COLOR
        self.Autoscroll = autoscroll
        self.Disabled = disabled
        self.ChangeSubmits = change_submits or enable_events
        self.RightClickMenu = right_click_menu
        self.BorderWidth = border_width if border_width is not None else DEFAULT_BORDER_WIDTH

        super().__init__(ELEM_TYPE_INPUT_MULTILINE, size=size, auto_size_text=auto_size_text, background_color=bg,
                         text_color=fg, key=key, pad=pad, tooltip=tooltip, font=font or DEFAULT_FONT, visible=visible)
        return

    def Update(self, value=None, disabled=None, append=False, font=None, text_color=None, background_color=None,
               visible=None, autoscroll=None):
        """

        :param value:  (Default value = None)
        :param disabled: disable or enable state of the element (Default value = None)
        :param append:  (Default value = False)
        :param font: (common_key) specifies the font family, size, etc (Default value = None)
        :param text_color: color of the text (Default value = None)
        :param background_color: color of background (Default value = None)
        :param visible:  change visibility of element (Default value = None)
        :param autoscroll:  (Default value = None)

        """
        
        if autoscroll is not None:
            self.Autoscroll = autoscroll
        if value is not None:
            if self.Disabled:
                self.TKText.configure(state='normal')
            try:
                if not append:
                    self.TKText.delete('1.0', tk.END)
                self.TKText.insert(tk.END, value)
            except:
                pass
            if self.Disabled:
                self.TKText.configure(state='disabled')
            self.DefaultText = value
        if self.Autoscroll:
            self.TKText.see(tk.END)
        if disabled == True:
            self.TKText.configure(state='disabled')
        elif disabled == False:
            self.TKText.configure(state='normal')
        if background_color is not None:
            self.TKText.configure(background=background_color)
        if text_color is not None:
            self.TKText.configure(fg=text_color)
        if font is not None:
            self.TKText.configure(font=font)
        if visible is False:
            self.TKText.pack_forget()
        elif visible is True:
            self.TKText.pack()

    def Get(self):
        """ """
        return self.TKText.get(1.0, tk.END)

    def SetFocus(self):
        """ """
        try:
            self.TKText.focus_set()
        except:
            pass

    def __del__(self):
        """ """
        super().__del__()


# ---------------------------------------------------------------------- #
#                                       Text                             #
# ---------------------------------------------------------------------- #
class Text(Element):
    """ """
    
    def __init__(self, text, size=(None, None), auto_size_text=None, click_submits=False, enable_events=False,
                 relief=None, font=None, text_color=None, background_color=None, justification=None, pad=None, key=None,
                 right_click_menu=None, tooltip=None, visible=True):
        """

        :param text: 
        :param size: (common_key) (w,h) w=characters-wide, h=rows-high (Default value = (None, None))
        :param auto_size_text: True if size should fit the text length (Default value = None)
        :param click_submits:  (Default value = False)
        :param enable_events: Turns on the element specific events.(Default value = False)
        :param relief:  (Default value = None)
        :param font: (common_key) specifies the font family, size, etc (Default value = None)
        :param text_color: color of the text (Default value = None)
        :param background_color: color of background (Default value = None)
        :param justification: justification for data display (Default value = None)
        :param pad: (common_key) Amount of padding to put around element (Default value = None)
        :param key: (common_key) Used with window.FindElement and with return values (Default value = None)
        :param right_click_menu: see "Right Click Menus" (Default value = None)
        :param tooltip: text, that will appear the you hover on (Default value = None)
        :param visible: set visibility state of the element (Default value = True)

        """
        
        self.DisplayText = str(text)
        self.TextColor = text_color if text_color else DEFAULT_TEXT_COLOR
        self.Justification = justification
        self.Relief = relief
        self.ClickSubmits = click_submits or enable_events
        if background_color is None:
            bg = DEFAULT_TEXT_ELEMENT_BACKGROUND_COLOR
        else:
            bg = background_color
        self.RightClickMenu = right_click_menu
        self.TKRightClickMenu = None

        super().__init__(ELEM_TYPE_TEXT, size, auto_size_text, background_color=bg, font=font if font else DEFAULT_FONT,
                         text_color=self.TextColor, pad=pad, key=key, tooltip=tooltip, visible=visible)
        return

    def Update(self, value=None, background_color=None, text_color=None, font=None, visible=None):
        """

        :param value:  (Default value = None)
        :param background_color: color of background (Default value = None)
        :param text_color: color of the text (Default value = None)
        :param font: (common_key) specifies the font family, size, etc (Default value = None)
        :param visible:  change visibility of element (Default value = None)

        """
        
        if value is not None:
            self.DisplayText = value
            stringvar = self.TKStringVar
            stringvar.set(value)
        if background_color is not None:
            self.TKText.configure(background=background_color)
        if text_color is not None:
            self.TKText.configure(fg=text_color)
        if font is not None:
            self.TKText.configure(font=font)
        if visible is False:
            self.TKText.pack_forget()
        elif visible is True:
            self.TKText.pack()

    def __del__(self):
        """ """
        super().__del__()


# -------------------------  Text Element lazy functions  ------------------------- #
Txt = Text
T = Text


# ---------------------------------------------------------------------- #
#                                       StatusBar                        #
# ---------------------------------------------------------------------- #
class StatusBar(Element):
    """ """
    
    def __init__(self, text, size=(None, None), auto_size_text=None, click_submits=None, enable_events=False,
                 relief=RELIEF_SUNKEN, font=None, text_color=None, background_color=None, justification=None, pad=None,
                 key=None, tooltip=None, visible=True):
        """

        :param text: 
        :param size: (common_key) (w,h) w=characters-wide, h=rows-high (Default value = (None, None))
        :param auto_size_text: True if size should fit the text length (Default value = None)
        :param click_submits:  (Default value = None)
        :param enable_events: Turns on the element specific events.(Default value = False)
        :param relief:  (Default value = RELIEF_SUNKEN)
        :param font: (common_key) specifies the font family, size, etc (Default value = None)
        :param text_color: color of the text (Default value = None)
        :param background_color: color of background (Default value = None)
        :param justification: justification for data display (Default value = None)
        :param pad: (common_key) Amount of padding to put around element (Default value = None)
        :param key: (common_key) Used with window.FindElement and with return values (Default value = None)
        :param tooltip: text, that will appear the you hover on (Default value = None)
        :param visible: set visibility state of the element (Default value = True)

        """
        
        self.DisplayText = text
        self.TextColor = text_color if text_color else DEFAULT_TEXT_COLOR
        self.Justification = justification
        self.Relief = relief
        self.ClickSubmits = click_submits or enable_events
        if background_color is None:
            bg = DEFAULT_TEXT_ELEMENT_BACKGROUND_COLOR
        else:
            bg = background_color
        super().__init__(ELEM_TYPE_STATUSBAR, size=size, auto_size_text=auto_size_text, background_color=bg,
                         font=font or DEFAULT_FONT, text_color=self.TextColor, pad=pad, key=key, tooltip=tooltip,
                         visible=visible)
        return

    def Update(self, value=None, background_color=None, text_color=None, font=None, visible=None):
        """

        :param value:  (Default value = None)
        :param background_color: color of background (Default value = None)
        :param text_color: color of the text (Default value = None)
        :param font: (common_key) specifies the font family, size, etc (Default value = None)
        :param visible:  change visibility of element (Default value = None)

        """
        
        if value is not None:
            self.DisplayText = value
            stringvar = self.TKStringVar
            stringvar.set(value)
        if background_color is not None:
            self.TKText.configure(background=background_color)
        if text_color is not None:
            self.TKText.configure(fg=text_color)
        if font is not None:
            self.TKText.configure(font=font)
        if visible is False:
            self.TKText.pack_forget()
        elif visible is True:
            self.TKText.pack()

    def __del__(self):
        """ """
        super().__del__()


# ---------------------------------------------------------------------- #
#                       TKProgressBar                                    #
#  Emulate the TK ProgressBar using canvas and rectangles
# ---------------------------------------------------------------------- #

class TKProgressBar():
    """ """
    def __init__(self, root, max, length=400, width=DEFAULT_PROGRESS_BAR_SIZE[1], style=DEFAULT_PROGRESS_BAR_STYLE,
                 relief=DEFAULT_PROGRESS_BAR_RELIEF, border_width=DEFAULT_PROGRESS_BAR_BORDER_WIDTH,
                 orientation='horizontal', BarColor=(None, None), key=None):
        """

        :param root: 
        :param max: 
        :param length:  (Default value = 400)
        :param width:  (Default value = DEFAULT_PROGRESS_BAR_SIZE[1])
        :param style:  (Default value = DEFAULT_PROGRESS_BAR_STYLE)
        :param relief:  (Default value = DEFAULT_PROGRESS_BAR_RELIEF)
        :param border_width:  (Default value = DEFAULT_PROGRESS_BAR_BORDER_WIDTH)
        :param orientation:  (Default value = 'horizontal')
        :param BarColor:  (Default value = (None, None))
        :param key: (common_key) Used with window.FindElement and with return values (Default value = None)

        """

        self.Length = length
        self.Width = width
        self.Max = max
        self.Orientation = orientation
        self.Count = None
        self.PriorCount = 0

        if orientation[0].lower() == 'h':
            s = ttk.Style()
            s.theme_use(style)
            if BarColor != COLOR_SYSTEM_DEFAULT:
                s.configure(str(key) + "my.Horizontal.TProgressbar", background=BarColor[0], troughcolor=BarColor[1],
                            troughrelief=relief, borderwidth=border_width, thickness=width)
            else:
                s.configure(str(key) + "my.Horizontal.TProgressbar", troughrelief=relief, borderwidth=border_width,
                            thickness=width)

            self.TKProgressBarForReal = ttk.Progressbar(root, maximum=self.Max,
                                                        style=str(key) + 'my.Horizontal.TProgressbar', length=length,
                                                        orient=tk.HORIZONTAL, mode='determinate')
        else:
            s = ttk.Style()
            s.theme_use(style)
            if BarColor != COLOR_SYSTEM_DEFAULT:
                s.configure(str(length) + str(width) + "my.Vertical.TProgressbar", background=BarColor[0],
                            troughcolor=BarColor[1], troughrelief=relief, borderwidth=border_width, thickness=width)
            else:
                s.configure(str(length) + str(width) + "my.Vertical.TProgressbar", troughrelief=relief,
                            borderwidth=border_width, thickness=width)
            self.TKProgressBarForReal = ttk.Progressbar(root, maximum=self.Max,
                                                        style=str(length) + str(width) + 'my.Vertical.TProgressbar',
                                                        length=length, orient=tk.VERTICAL, mode='determinate')

    def Update(self, count=None, max=None):
        """

        :param count:  (Default value = None)
        :param max:  (Default value = None)

        """
        if max is not None:
            self.Max = max
            try:
                self.TKProgressBarForReal.config(maximum=max)
            except:
                return False
        if count is not None and count > self.Max: return False
        if count is not None:
            try:
                self.TKProgressBarForReal['value'] = count
            except:
                return False
        return True

    def __del__(self):
        """ """
        try:
            self.TKProgressBarForReal.__del__()
        except:
            pass


# ---------------------------------------------------------------------- #
#                           TKOutput                                     #
#   New Type of TK Widget that's a Text Widget in disguise               #
#       Note that it's inherited from the TKFrame class so that the      #
#       Scroll bar will span the length of the frame                     #
# ---------------------------------------------------------------------- #
class TKOutput(tk.Frame):
    """ """
    def __init__(self, parent, width, height, bd, background_color=None, text_color=None, font=None, pad=None):
        """

        :param parent: 
        :param width: 
        :param height: 
        :param bd: 
        :param background_color: color of background (Default value = None)
        :param text_color: color of the text (Default value = None)
        :param font: (common_key) specifies the font family, size, etc (Default value = None)
        :param pad: (common_key) Amount of padding to put around element (Default value = None)

        """
        self.frame = tk.Frame(parent)
        tk.Frame.__init__(self, self.frame)
        self.output = tk.Text(self.frame, width=width, height=height, bd=bd, font=font)
        if background_color and background_color != COLOR_SYSTEM_DEFAULT:
            self.output.configure(background=background_color)
            self.frame.configure(background=background_color)
        if text_color and text_color != COLOR_SYSTEM_DEFAULT:
            self.output.configure(fg=text_color)
        self.vsb = tk.Scrollbar(self.frame, orient="vertical", command=self.output.yview)
        self.output.configure(yscrollcommand=self.vsb.set)
        self.output.pack(side="left", fill="both", expand=True)
        self.vsb.pack(side="left", fill="y", expand=False)
        self.frame.pack(side="left", padx=pad[0], pady=pad[1], expand=True, fill='y')
        self.previous_stdout = sys.stdout
        self.previous_stderr = sys.stderr

        sys.stdout = self
        sys.stderr = self
        self.pack()

    def write(self, txt):
        """

        :param txt: 

        """
        try:
            self.output.insert(tk.END, str(txt))
            self.output.see(tk.END)
        except:
            pass

    def Close(self):
        """ """
        sys.stdout = self.previous_stdout
        sys.stderr = self.previous_stderr

    def flush(self):
        """ """
        sys.stdout = self.previous_stdout
        sys.stderr = self.previous_stderr

    def __del__(self):
        """ """
        sys.stdout = self.previous_stdout
        sys.stderr = self.previous_stderr


# ---------------------------------------------------------------------- #
#                           Output                                       #
#  Routes stdout, stderr to a scrolled window                            #
# ---------------------------------------------------------------------- #
class Output(Element):
    """ """
    
    def __init__(self, size=(None, None), background_color=None, text_color=None, pad=None, font=None, tooltip=None,
                 key=None, right_click_menu=None, visible=True):
        """

        :param size: (common_key) (w,h) w=characters-wide, h=rows-high (Default value = (None, None))
        :param background_color: color of background (Default value = None)
        :param text_color: color of the text (Default value = None)
        :param pad: (common_key) Amount of padding to put around element (Default value = None)
        :param font: (common_key) specifies the font family, size, etc (Default value = None)
        :param tooltip: text, that will appear the you hover on (Default value = None)
        :param key: (common_key) Used with window.FindElement and with return values (Default value = None)
        :param right_click_menu: see "Right Click Menus" (Default value = None)
        :param visible: set visibility state of the element (Default value = True)

        """
        
        self._TKOut = None
        bg = background_color if background_color else DEFAULT_INPUT_ELEMENTS_COLOR
        fg = text_color if text_color is not None else DEFAULT_INPUT_TEXT_COLOR
        self.RightClickMenu = right_click_menu

        super().__init__(ELEM_TYPE_OUTPUT, size=size, background_color=bg, text_color=fg, pad=pad, font=font,
                         tooltip=tooltip, key=key, visible=visible)

    @property
    def TKOut(self):
        """ """
        if self._TKOut is None:
            print('*** Did you forget to call Finalize()? Your code should look something like: ***')
            print('*** form = sg.Window("My Form").Layout(layout).Finalize() ***')
        return self._TKOut

    def Update(self, value=None, visible=None):
        """

        :param value:  (Default value = None)
        :param visible:  change visibility of element (Default value = None)

        """
        
        if value is not None:
            self._TKOut.output.delete('1.0', tk.END)
            self._TKOut.output.insert(tk.END, value)
        if visible is False:
            self._TKOut.frame.pack_forget()
        elif visible is True:
            self._TKOut.frame.pack()

    def __del__(self):
        """ """
        try:
            self._TKOut.__del__()
        except:
            pass
        super().__del__()


# ---------------------------------------------------------------------- #
#                           Button Class                                 #
# ---------------------------------------------------------------------- #
class Button(Element):
    """ """
    
    def __init__(self, button_text='', button_type=BUTTON_TYPE_READ_FORM, target=(None, None), tooltip=None,
                 file_types=(("ALL Files", "*.*"),), initial_folder=None, disabled=False, change_submits=False,
                 enable_events=False, image_filename=None, image_data=None, image_size=(None, None),
                 image_subsample=None, border_width=None, size=(None, None), auto_size_button=None, button_color=None,
                 font=None, bind_return_key=False, focus=False, pad=None, key=None, visible=True):
        """

        :param button_text:  (Default value = '')
        :param button_type:  (Default value = BUTTON_TYPE_READ_FORM)
        :param target: 
        :param tooltip: text, that will appear the you hover on (Default value = None)
        :param file_types:  (Default value = (("ALL Files", "*.*"),))
        :param initial_folder:  (Default value = None)
        :param disabled: set disable state for element (Default value = False)
        :param change_submits: If True, pressing Enter key submits window (Default value = False)
        :param enable_events: Turns on the element specific events.(Default value = False)
        :param image_filename:  (Default value = None)
        :param image_data:  (Default value = None)
        :param image_size:  (Default value = (None)
        :param image_subsample:  (Default value = None)
        :param border_width:  (Default value = None)
        :param size: (common_key) (w,h) w=characters-wide, h=rows-high (Default value = (None)
        :param auto_size_button:  (Default value = None)
        :param button_color:  (Default value = None)
        :param font: (common_key) specifies the font family, size, etc (Default value = None)
        :param bind_return_key:  (Default value = False)
        :param focus: if focus should be set to this (Default value = None)
        :param pad: (common_key) Amount of padding to put around element (Default value = None)
        :param key: (common_key) Used with window.FindElement and with return values (Default value = None)
        :param visible: set visibility state of the element (Default value = True)

        """
        
        self.AutoSizeButton = auto_size_button
        self.BType = button_type
        self.FileTypes = file_types
        self.TKButton = None  # type: tk.Button
        self.Target = target
        self.ButtonText = str(button_text)
        if sys.platform == 'darwin' and button_color is not None:
            print('Button *** WARNING - Button colors are not supported on the Mac ***')
        self.ButtonColor = button_color if button_color else DEFAULT_BUTTON_COLOR
        self.ImageFilename = image_filename
        self.ImageData = image_data
        self.ImageSize = image_size
        self.ImageSubsample = image_subsample
        self.UserData = None
        self.BorderWidth = border_width if border_width is not None else DEFAULT_BORDER_WIDTH
        self.BindReturnKey = bind_return_key
        self.Focus = focus
        self.TKCal = None
        self.CalendarCloseWhenChosen = None
        self.DefaultDate_M_D_Y = (None, None, None)
        self.InitialFolder = initial_folder
        self.Disabled = disabled
        self.ChangeSubmits = change_submits or enable_events

        super().__init__(ELEM_TYPE_BUTTON, size=size, font=font, pad=pad, key=key, tooltip=tooltip, visible=visible)
        return

    # Realtime button release callback
    def ButtonReleaseCallBack(self, parm):
        """

        :param parm: 

        """
        self.LastButtonClickedWasRealtime = False
        self.ParentForm.LastButtonClicked = None

    # Realtime button callback
    def ButtonPressCallBack(self, parm):
        """

        :param parm: 

        """
        self.ParentForm.LastButtonClickedWasRealtime = True
        if self.Key is not None:
            self.ParentForm.LastButtonClicked = self.Key
        else:
            self.ParentForm.LastButtonClicked = self.ButtonText
        if self.ParentForm.CurrentlyRunningMainloop:
            self.ParentForm.TKroot.quit()  # kick out of loop if read was called

    # -------  Button Callback  ------- #
    def ButtonCallBack(self):
        """ """
        # global _my_windows

        # print('Button callback')

        # print(f'Parent = {self.ParentForm}   Position = {self.Position}')
        # Buttons modify targets or return from the form
        # If modifying target, get the element object at the target and modify its StrVar
        target = self.Target
        target_element = None
        if target[0] == ThisRow:
            target = [self.Position[0], target[1]]
            if target[1] < 0:
                target[1] = self.Position[1] + target[1]
        strvar = None
        should_submit_window = False
        if target == (None, None):
            strvar = self.TKStringVar
        else:
            if not isinstance(target, str):
                if target[0] < 0:
                    target = [self.Position[0] + target[0], target[1]]
                target_element = self.ParentContainer._GetElementAtLocation(target)
            else:
                target_element = self.ParentForm.FindElement(target)
            try:
                strvar = target_element.TKStringVar
            except:
                pass
            try:
                if target_element.ChangeSubmits:
                    should_submit_window = True
            except:
                pass
        filetypes = (("ALL Files", "*.*"),) if self.FileTypes is None else self.FileTypes
        if self.BType == BUTTON_TYPE_BROWSE_FOLDER:
            folder_name = tk.filedialog.askdirectory(initialdir=self.InitialFolder)  # show the 'get folder' dialog box
            if folder_name != '':
                try:
                    strvar.set(folder_name)
                    self.TKStringVar.set(folder_name)
                except:
                    pass
        elif self.BType == BUTTON_TYPE_BROWSE_FILE:
            if sys.platform == 'darwin':
                file_name = tk.filedialog.askopenfilename(
                    initialdir=self.InitialFolder)  # show the 'get file' dialog box
            else:
                file_name = tk.filedialog.askopenfilename(filetypes=filetypes,
                                                          initialdir=self.InitialFolder)  # show the 'get file' dialog box
            if file_name != '':
                strvar.set(file_name)
                self.TKStringVar.set(file_name)
        elif self.BType == BUTTON_TYPE_COLOR_CHOOSER:
            color = tk.colorchooser.askcolor()  # show the 'get file' dialog box
            color = color[1]  # save only the #RRGGBB portion
            strvar.set(color)
            self.TKStringVar.set(color)
        elif self.BType == BUTTON_TYPE_BROWSE_FILES:
            if sys.platform == 'darwin':
                file_name = tk.filedialog.askopenfilenames(initialdir=self.InitialFolder)
            else:
                file_name = tk.filedialog.askopenfilenames(filetypes=filetypes, initialdir=self.InitialFolder)
            if file_name != '':
                file_name = ';'.join(file_name)
                strvar.set(file_name)
                self.TKStringVar.set(file_name)
        elif self.BType == BUTTON_TYPE_SAVEAS_FILE:
            if sys.platform == 'darwin':
                file_name = tk.filedialog.asksaveasfilename(
                    initialdir=self.InitialFolder)  # show the 'get file' dialog box
            else:
                file_name = tk.filedialog.asksaveasfilename(filetypes=filetypes,
                                                            initialdir=self.InitialFolder)  # show the 'get file' dialog box
            if file_name != '':
                strvar.set(file_name)
                self.TKStringVar.set(file_name)
        elif self.BType == BUTTON_TYPE_CLOSES_WIN:  # this is a return type button so GET RESULTS and destroy window
            # first, get the results table built
            # modify the Results table in the parent FlexForm object
            if self.Key is not None:
                self.ParentForm.LastButtonClicked = self.Key
            else:
                self.ParentForm.LastButtonClicked = self.ButtonText
            self.ParentForm.FormRemainedOpen = False
            self.ParentForm._Close()
            if self.ParentForm.CurrentlyRunningMainloop:
                self.ParentForm.TKroot.quit()
            if self.ParentForm.NonBlocking:
                self.ParentForm.TKroot.destroy()
                Window.DecrementOpenCount()
        elif self.BType == BUTTON_TYPE_READ_FORM:  # LEAVE THE WINDOW OPEN!! DO NOT CLOSE
            # first, get the results table built
            # modify the Results table in the parent FlexForm object
            if self.Key is not None:
                self.ParentForm.LastButtonClicked = self.Key
            else:
                self.ParentForm.LastButtonClicked = self.ButtonText
            self.ParentForm.FormRemainedOpen = True
            if self.ParentForm.CurrentlyRunningMainloop:  # if this window is running the mainloop, kick out
                self.ParentForm.TKroot.quit()  # kick the users out of the mainloop
        elif self.BType == BUTTON_TYPE_CLOSES_WIN_ONLY:  # special kind of button that does not exit main loop
            self.ParentForm._Close()
            if self.ParentForm.NonBlocking:
                self.ParentForm.TKroot.destroy()
                Window.DecrementOpenCount()
        elif self.BType == BUTTON_TYPE_CALENDAR_CHOOSER:  # this is a return type button so GET RESULTS and destroy window
            should_submit_window = False
            root = tk.Toplevel()
            root.title('Calendar Chooser')
            root.wm_attributes("-topmost", 1)
            self.TKCal = TKCalendar(master=root, firstweekday=calendar.SUNDAY, target_element=target_element,
                                    close_when_chosen=self.CalendarCloseWhenChosen, default_date=self.DefaultDate_M_D_Y,
                                    locale=self.CalendarLocale, format=self.CalendarFormat)
            self.TKCal.pack(expand=1, fill='both')
            root.update()

            if type(Window.user_defined_icon) is bytes:
                calendar_icon = tkinter.PhotoImage(data=Window.user_defined_icon)
            else:
                calendar_icon = tkinter.PhotoImage(data=DEFAULT_BASE64_ICON)
            try:
                root.tk.call('wm', 'iconphoto', root._w, calendar_icon)
            except:
                pass
        elif self.BType == BUTTON_TYPE_SHOW_DEBUGGER:
            if self.ParentForm.DebuggerEnabled:
                Debugger.debugger._build_floating_window()
                # show_debugger_window()

        if should_submit_window:
            self.ParentForm.LastButtonClicked = target_element.Key
            self.ParentForm.FormRemainedOpen = True
            if self.ParentForm.CurrentlyRunningMainloop:
                self.ParentForm.TKroot.quit()  # kick the users out of the mainloop

        return

    def Update(self, text=None, button_color=(None, None), disabled=None, image_data=None, image_filename=None,
               visible=None, image_subsample=None, image_size=None):
        """

        :param text:  (Default value = None)
        :param button_color:  (Default value = (None)
        :param disabled: disable or enable state of the element (Default value = None)
        :param image_data:  (Default value = None)
        :param image_filename:  (Default value = None)
        :param visible:  change visibility of element (Default value = None)
        :param image_subsample:  (Default value = None)
        :param image_size:  (Default value = None)

        """
        
        try:
            if text is not None:
                self.TKButton.configure(text=text)
                self.ButtonText = text
            if sys.platform == 'darwin' and button_color != (None, None):
                print('Button.Update *** WARNING - Button colors are not supported on the Mac***')
            if button_color != (None, None):
                self.TKButton.config(foreground=button_color[0], background=button_color[1])
                self.ButtonColor = button_color
        except:
            return
        if disabled == True:
            self.TKButton['state'] = 'disabled'
        elif disabled == False:
            self.TKButton['state'] = 'normal'
        if image_data is not None:
            image = tk.PhotoImage(data=image_data)
            if image_size is not None:
                width, height = image_size
            else:
                width, height = image.width(), image.height()
            if image_subsample:
                image = image.subsample(image_subsample)
            self.TKButton.config(image=image, width=width, height=height)
            self.TKButton.image = image
        if image_filename is not None:
            self.TKButton.config(highlightthickness=0)
            image = tk.PhotoImage(file=image_filename)
            if image_size is not None:
                width, height = image_size
            else:
                width, height = image.width(), image.height()
            if image_subsample:
                image = image.subsample(image_subsample)
            self.TKButton.config(image=image, width=width, height=height)
            self.TKButton.image = image
        if visible is False:
            self.TKButton.pack_forget()
        elif visible is True:
            self.TKButton.pack()

    def GetText(self):
        """ """
        return self.ButtonText

    def SetFocus(self):
        """ """
        try:
            self.TKButton.focus_set()
        except:
            pass

    def Click(self):
        """Generates a click of the button as if the user clicked the button
        :return:


        """
        try:
            self.TKButton.invoke()
        except:
            print('Exception clicking button')

    def __del__(self):
        """ """
        try:
            self.TKButton.__del__()
        except:
            pass
        super().__del__()


# -------------------------  Button lazy functions  ------------------------- #
B = Button
Btn = Button
Butt = Button


# ---------------------------------------------------------------------- #
#                           ButtonMenu Class                             #
# ---------------------------------------------------------------------- #
class ButtonMenu(Element):
    """ """
    
    def __init__(self, button_text, menu_def, tooltip=None, disabled=False,
                 image_filename=None, image_data=None, image_size=(None, None), image_subsample=None, border_width=None,
                 size=(None, None), auto_size_button=None, button_color=None, font=None, pad=None, key=None,
                 tearoff=False, visible=True):
        """

        :param button_text: 
        :param menu_def: 
        :param tooltip: text, that will appear the you hover on (Default value = None)
        :param disabled: set disable state for element (Default value = False)
        :param image_filename:  (Default value = None)
        :param image_data:  (Default value = None)
        :param image_size:  (Default value = (None, None))
        :param image_subsample:  (Default value = None)
        :param border_width:  (Default value = None)
        :param size: (common_key) (w,h) w=characters-wide, h=rows-high (Default value = (None)
        :param auto_size_button:  (Default value = None)
        :param button_color:  (Default value = None)
        :param font: (common_key) specifies the font family, size, etc (Default value = None)
        :param pad: (common_key) Amount of padding to put around element (Default value = None)
        :param key: (common_key) Used with window.FindElement and with return values (Default value = None)
        :param tearoff:  (Default value = False)
        :param visible: set visibility state of the element (Default value = True)

        """
        
        self.MenuDefinition = menu_def
        self.AutoSizeButton = auto_size_button
        self.ButtonText = button_text
        self.ButtonColor = button_color if button_color else DEFAULT_BUTTON_COLOR
        self.TextColor = self.ButtonColor[0]
        self.BackgroundColor = self.ButtonColor[1]
        self.BorderWidth = border_width
        self.ImageFilename = image_filename
        self.ImageData = image_data
        self.ImageSize = image_size
        self.ImageSubsample = image_subsample
        self.Disabled = disabled
        self.IsButtonMenu = True
        self.MenuItemChosen = None
        self.Tearoff = tearoff
        self.TKButtonMenu = None
        self.TKMenu = None
        # self.temp_size = size if size != (NONE, NONE) else

        super().__init__(ELEM_TYPE_BUTTONMENU, size=size, font=font, pad=pad, key=key, tooltip=tooltip,
                         text_color=self.TextColor, background_color=self.BackgroundColor, visible=visible)
        return

    def _MenuItemChosenCallback(self, item_chosen):  # ButtonMenu Menu Item Chosen Callback
        """

        :param item_chosen: 

        """
        # print('IN MENU ITEM CALLBACK', item_chosen)
        self.MenuItemChosen = item_chosen.replace('&', '')
        self.ParentForm.LastButtonClicked = self.Key
        self.ParentForm.FormRemainedOpen = True
        if self.ParentForm.CurrentlyRunningMainloop:
            self.ParentForm.TKroot.quit()  # kick the users out of the mainloop

    def Update(self, menu_definition, visible=None):
        """

        :param menu_definition: 
        :param visible:  change visibility of element (Default value = None)

        """
        
        self.MenuDefinition = menu_definition
        if menu_definition is not None:
            self.TKMenu = tk.Menu(self.TKButtonMenu, tearoff=self.Tearoff)  # create the menubar
            AddMenuItem(self.TKMenu, menu_definition[1], self)
        self.TKButtonMenu.configure(menu=self.TKMenu)
        if visible is False:
            self.TKButtonMenu.pack_forget()
        elif visible is True:
            self.TKButtonMenu.pack()

    def __del__(self):
        """ """
        try:
            self.TKButton.__del__()
        except:
            pass
        super().__del__()


# ---------------------------------------------------------------------- #
#                           ProgreessBar                                 #
# ---------------------------------------------------------------------- #
class ProgressBar(Element):
    """ """
    def __init__(self, max_value, orientation=None, size=(None, None), auto_size_text=None, bar_color=(None, None),
                 style=None, border_width=None, relief=None, key=None, pad=None, visible=True):
        """

        :param max_value: 
        :param orientation:  (Default value = None)
        :param size: (common_key) (w,h) w=characters-wide, h=rows-high (Default value = (None, None))
        :param auto_size_text: True if size should fit the text length (Default value = None)
        :param bar_color:  (Default value = (None)
        :param style:  (Default value = None)
        :param border_width:  (Default value = None)
        :param relief:  (Default value = None)
        :param key: (common_key) Used with window.FindElement and with return values (Default value = None)
        :param pad: (common_key) Amount of padding to put around element (Default value = None)
        :param visible: set visibility state of the element (Default value = True)

        """
        
        self.MaxValue = max_value
        self.TKProgressBar = None
        self.Cancelled = False
        self.NotRunning = True
        self.Orientation = orientation if orientation else DEFAULT_METER_ORIENTATION
        self.BarColor = bar_color
        self.BarStyle = style if style else DEFAULT_PROGRESS_BAR_STYLE
        self.BorderWidth = border_width if border_width else DEFAULT_PROGRESS_BAR_BORDER_WIDTH
        self.Relief = relief if relief else DEFAULT_PROGRESS_BAR_RELIEF
        self.BarExpired = False
        super().__init__(ELEM_TYPE_PROGRESS_BAR, size=size, auto_size_text=auto_size_text, key=key, pad=pad,
                         visible=visible)

    # returns False if update failed
    def UpdateBar(self, current_count, max=None):
        """

        :param current_count: 
        :param max:  (Default value = None)

        """
        
        if self.ParentForm.TKrootDestroyed:
            return False
        self.TKProgressBar.Update(current_count, max=max)
        try:
            self.ParentForm.TKroot.update()
        except:
            Window.DecrementOpenCount()
            # _my_windows.Decrement()
            return False
        return True

    def Update(self, visible=None):
        """

        :param visible:  change visibility of element (Default value = None)

        """
        
        if visible is False:
            self.TKProgressBar.TKProgressBarForReal.pack_forget()
        elif visible is True:
            self.TKProgressBar.TKProgressBarForReal.pack()

    def __del__(self):
        """ """
        try:
            self.TKProgressBar.__del__()
        except:
            pass
        super().__del__()


# ---------------------------------------------------------------------- #
#                           Image                                        #
# ---------------------------------------------------------------------- #
class Image(Element):
    """ """
    
    def __init__(self, filename=None, data=None, background_color=None, size=(None, None), pad=None, key=None,
                 tooltip=None, right_click_menu=None, visible=True, enable_events=False):
        """

        :param filename:  (Default value = None)
        :param data:  (Default value = None)
        :param background_color: color of background (Default value = None)
        :param size: (common_key) (w,h) w=characters-wide, h=rows-high (Default value = (None, None))
        :param pad: (common_key) Amount of padding to put around element (Default value = None)
        :param key: (common_key) Used with window.FindElement and with return values (Default value = None)
        :param tooltip: text, that will appear the you hover on (Default value = None)
        :param right_click_menu: see "Right Click Menus" (Default value = None)
        :param visible: set visibility state of the element (Default value = True)
        :param enable_events: Turns on the element specific events.(Default value = False)

        """
        
        self.Filename = filename
        self.Data = data
        self.tktext_label = None
        self.BackgroundColor = background_color
        if data is None and filename is None:
            print('* Warning... no image specified in Image Element! *')
        self.EnableEvents = enable_events
        self.RightClickMenu = right_click_menu
        self.AnimatedFrames = None
        self.CurrentFrameNumber = 0
        self.TotalAnimatedFrames = 0
        self.LastFrameTime = 0
        self.Source = filename if filename is not None else data

        super().__init__(ELEM_TYPE_IMAGE, size=size, background_color=background_color, pad=pad, key=key,
                         tooltip=tooltip, visible=visible)
        return

    def Update(self, filename=None, data=None, size=(None, None), visible=None):
        """

        :param filename:  (Default value = None)
        :param data:  (Default value = None)
        :param size: (common_key) (w,h) w=characters-wide, h=rows-high (Default value = (None, None))
        :param visible:  change visibility of element (Default value = None)

        """
        
        if filename is not None:
            image = tk.PhotoImage(file=filename)
        elif data is not None:
            # if type(data) is bytes:
            try:
                image = tk.PhotoImage(data=data)
            except:
                return  # an error likely means the window has closed so exit
        else:
            return
        width, height = size[0] or image.width(), size[1] or image.height()
        try:  # sometimes crashes if user closed with X
            self.tktext_label.configure(image=image, width=width, height=height)
        except:
            pass
        self.tktext_label.image = image
        if visible is False:
            self.tktext_label.pack_forget()
        elif visible is True:
            self.tktext_label.pack()

    def UpdateAnimation(self, source, time_between_frames=0):
        """

        :param source: 
        :param time_between_frames:  (Default value = 0)

        """
        
        if self.Source != source:
            self.AnimatedFrames = None
            self.Source = source

        if self.AnimatedFrames is None:
            self.TotalAnimatedFrames = 0
            self.AnimatedFrames = []
            for i in range(1000):
                if type(source) is not bytes:
                    try:
                        self.AnimatedFrames.append(tk.PhotoImage(file=source, format='gif -index %i' % (i)))
                    except:
                        break
                else:
                    try:
                        self.AnimatedFrames.append(tk.PhotoImage(data=source, format='gif -index %i' % (i)))
                    except:
                        break
                self.TotalAnimatedFrames += 1
            self.LastFrameTime = time.time()
            self.CurrentFrameNumber = 0
        # show the frame

        now = time.time()

        if time_between_frames:
            if (now - self.LastFrameTime) * 1000 > time_between_frames:
                self.LastFrameTime = now
                self.CurrentFrameNumber = self.CurrentFrameNumber + 1 if self.CurrentFrameNumber + 1 < self.TotalAnimatedFrames else 0
            else:  # don't reshow the frame again if not time for new frame
                return
        else:
            self.CurrentFrameNumber = self.CurrentFrameNumber + 1 if self.CurrentFrameNumber + 1 < self.TotalAnimatedFrames else 0
        image = self.AnimatedFrames[self.CurrentFrameNumber]
        try:  # needed in case the window was closed with an "X"
            self.tktext_label.configure(image=image, width=image.width(), heigh=image.height())
        except:
            pass

    def __del__(self):
        """ """
        super().__del__()


# ---------------------------------------------------------------------- #
#                           Canvas                                       #
# ---------------------------------------------------------------------- #
class Canvas(Element):
    """ """
    
    def __init__(self, canvas=None, background_color=None, size=(None, None), pad=None, key=None, tooltip=None,
                 right_click_menu=None, visible=True):
        """

        :param canvas:  (Default value = None)
        :param background_color: color of background (Default value = None)
        :param size: (common_key) (w,h) w=characters-wide, h=rows-high (Default value = (None, None))
        :param pad: (common_key) Amount of padding to put around element (Default value = None)
        :param key: (common_key) Used with window.FindElement and with return values (Default value = None)
        :param tooltip: text, that will appear the you hover on (Default value = None)
        :param right_click_menu: see "Right Click Menus" (Default value = None)
        :param visible: set visibility state of the element (Default value = True)

        """
        
        self.BackgroundColor = background_color if background_color is not None else DEFAULT_BACKGROUND_COLOR
        self._TKCanvas = canvas
        self.RightClickMenu = right_click_menu

        super().__init__(ELEM_TYPE_CANVAS, background_color=background_color, size=size, pad=pad, key=key,
                         tooltip=tooltip, visible=visible)
        return

    @property
    def TKCanvas(self):
        """ """
        if self._TKCanvas is None:
            print('*** Did you forget to call Finalize()? Your code should look something like: ***')
            print('*** form = sg.Window("My Form").Layout(layout).Finalize() ***')
        return self._TKCanvas

    def __del__(self):
        """ """
        super().__del__()


# ---------------------------------------------------------------------- #
#                           Graph                                        #
# ---------------------------------------------------------------------- #
class Graph(Element):
    """ """
    
    def __init__(self, canvas_size, graph_bottom_left, graph_top_right, background_color=None, pad=None,
                 change_submits=False, drag_submits=False, enable_events=False, key=None, tooltip=None,
                 right_click_menu=None, visible=True):
        """

        :param canvas_size: 
        :param graph_bottom_left: 
        :param graph_top_right: 
        :param background_color: color of background (Default value = None)
        :param pad: (common_key) Amount of padding to put around element (Default value = None)
        :param change_submits: If True, pressing Enter key submits window (Default value = False)
        :param drag_submits:  (Default value = False)
        :param enable_events: Turns on the element specific events.(Default value = False)
        :param key: (common_key) Used with window.FindElement and with return values (Default value = None)
        :param tooltip: text, that will appear the you hover on (Default value = None)
        :param right_click_menu: see "Right Click Menus" (Default value = None)
        :param visible: set visibility state of the element (Default value = True)

        """
        
        self.CanvasSize = canvas_size
        self.BottomLeft = graph_bottom_left
        self.TopRight = graph_top_right
        # self._TKCanvas = None               # type: tk.Canvas
        self._TKCanvas2 = None  # type: tk.Canvas
        self.ChangeSubmits = change_submits or enable_events
        self.DragSubmits = drag_submits
        self.ClickPosition = (None, None)
        self.MouseButtonDown = False
        self.Images = {}
        self.RightClickMenu = right_click_menu

        super().__init__(ELEM_TYPE_GRAPH, background_color=background_color, size=canvas_size, pad=pad, key=key,
                         tooltip=tooltip, visible=visible)
        return

    def _convert_xy_to_canvas_xy(self, x_in, y_in):
        """

        :param x_in: 
        :param y_in: 

        """
        if None in (x_in, y_in):
            return None, None
        scale_x = (self.CanvasSize[0] - 0) / (self.TopRight[0] - self.BottomLeft[0])
        scale_y = (0 - self.CanvasSize[1]) / (self.TopRight[1] - self.BottomLeft[1])
        new_x = 0 + scale_x * (x_in - self.BottomLeft[0])
        new_y = self.CanvasSize[1] + scale_y * (y_in - self.BottomLeft[1])
        return new_x, new_y

    def _convert_canvas_xy_to_xy(self, x_in, y_in):
        """

        :param x_in: 
        :param y_in: 

        """
        if None in (x_in, y_in):
            return None, None
        scale_x = (self.CanvasSize[0] - 0) / (self.TopRight[0] - self.BottomLeft[0])
        scale_y = (0 - self.CanvasSize[1]) / (self.TopRight[1] - self.BottomLeft[1])

        new_x = x_in / scale_x + self.BottomLeft[0]
        new_y = (y_in - self.CanvasSize[1]) / scale_y + self.BottomLeft[1]
        return int(new_x), int(new_y)

    def DrawLine(self, point_from, point_to, color='black', width=1):
        """

        :param point_from: 
        :param point_to: 
        :param color:  (Default value = 'black')
        :param width:  (Default value = 1)

        """
        if point_from == (None, None):
            return
        converted_point_from = self._convert_xy_to_canvas_xy(point_from[0], point_from[1])
        converted_point_to = self._convert_xy_to_canvas_xy(point_to[0], point_to[1])
        if self._TKCanvas2 is None:
            print('*** WARNING - The Graph element has not been finalized and cannot be drawn upon ***')
            print('Call Window.Finalize() prior to this operation')
            return None
        try:  # in case window was closed with an X
            id = self._TKCanvas2.create_line(converted_point_from, converted_point_to, width=width, fill=color)
        except:
            id = None
        return id

    def DrawPoint(self, point, size=2, color='black'):
        """

        :param point: 
        :param size: (common_key) (w,h) w=characters-wide, h=rows-high (Default value = 2)
        :param color:  (Default value = 'black')

        """
        if point == (None, None):
            return
        converted_point = self._convert_xy_to_canvas_xy(point[0], point[1])
        if self._TKCanvas2 is None:
            print('*** WARNING - The Graph element has not been finalized and cannot be drawn upon ***')
            print('Call Window.Finalize() prior to this operation')
            return None
        try:  # needed in case window was closed with an X
            id = self._TKCanvas2.create_oval(converted_point[0] - size, converted_point[1] - size,
                                             converted_point[0] + size, converted_point[1] + size, fill=color,
                                             outline=color)
        except:
            id = None
        return

    def DrawCircle(self, center_location, radius, fill_color=None, line_color='black'):
        """

        :param center_location: 
        :param radius: 
        :param fill_color:  (Default value = None)
        :param line_color:  (Default value = 'black')

        """
        if center_location == (None, None):
            return
        converted_point = self._convert_xy_to_canvas_xy(center_location[0], center_location[1])
        if self._TKCanvas2 is None:
            print('*** WARNING - The Graph element has not been finalized and cannot be drawn upon ***')
            print('Call Window.Finalize() prior to this operation')
            return None
        try:  # needed in case the window was closed with an X
            id = self._TKCanvas2.create_oval(converted_point[0] - radius, converted_point[1] - radius,
                                             converted_point[0] + radius, converted_point[1] + radius, fill=fill_color,
                                             outline=line_color)
        except:
            id = None
        return id

    def DrawOval(self, top_left, bottom_right, fill_color=None, line_color=None):
        """

        :param top_left: 
        :param bottom_right: 
        :param fill_color:  (Default value = None)
        :param line_color:  (Default value = None)

        """
        converted_top_left = self._convert_xy_to_canvas_xy(top_left[0], top_left[1])
        converted_bottom_right = self._convert_xy_to_canvas_xy(bottom_right[0], bottom_right[1])
        if self._TKCanvas2 is None:
            print('*** WARNING - The Graph element has not been finalized and cannot be drawn upon ***')
            print('Call Window.Finalize() prior to this operation')
            return None
        try:  # in case windows close with X
            id = self._TKCanvas2.create_oval(converted_top_left[0], converted_top_left[1], converted_bottom_right[0],
                                             converted_bottom_right[1], fill=fill_color, outline=line_color)
        except:
            id = None

        return id

    def DrawArc(self, top_left, bottom_right, extent, start_angle, style=None, arc_color='black'):
        """

        :param top_left: 
        :param bottom_right: 
        :param extent: 
        :param start_angle: 
        :param style:  (Default value = None)
        :param arc_color:  (Default value = 'black')

        """
        converted_top_left = self._convert_xy_to_canvas_xy(top_left[0], top_left[1])
        converted_bottom_right = self._convert_xy_to_canvas_xy(bottom_right[0], bottom_right[1])
        tkstyle = tk.PIESLICE if style is None else style
        if self._TKCanvas2 is None:
            print('*** WARNING - The Graph element has not been finalized and cannot be drawn upon ***')
            print('Call Window.Finalize() prior to this operation')
            return None
        try:  # in case closed with X
            id = self._TKCanvas2.create_arc(converted_top_left[0], converted_top_left[1], converted_bottom_right[0],
                                            converted_bottom_right[1], extent=extent, start=start_angle, style=tkstyle,
                                            outline=arc_color)
        except:
            id = None
        return id

    def DrawRectangle(self, top_left, bottom_right, fill_color=None, line_color=None):
        """

        :param top_left: 
        :param bottom_right: 
        :param fill_color:  (Default value = None)
        :param line_color:  (Default value = None)

        """
        converted_top_left = self._convert_xy_to_canvas_xy(top_left[0], top_left[1])
        converted_bottom_right = self._convert_xy_to_canvas_xy(bottom_right[0], bottom_right[1])
        if self._TKCanvas2 is None:
            print('*** WARNING - The Graph element has not been finalized and cannot be drawn upon ***')
            print('Call Window.Finalize() prior to this operation')
            return None
        try:  # in case closed with X
            id = self._TKCanvas2.create_rectangle(converted_top_left[0], converted_top_left[1],
                                                  converted_bottom_right[0],
                                                  converted_bottom_right[1], fill=fill_color, outline=line_color)
        except:
            id = None
        return id

    def DrawText(self, text, location, color='black', font=None, angle=0):
        """

        :param text: 
        :param location: 
        :param color:  (Default value = 'black')
        :param font: (common_key) specifies the font family, size, etc (Default value = None)
        :param angle:  (Default value = 0)

        """
        if location == (None, None):
            return
        converted_point = self._convert_xy_to_canvas_xy(location[0], location[1])
        if self._TKCanvas2 is None:
            print('*** WARNING - The Graph element has not been finalized and cannot be drawn upon ***')
            print('Call Window.Finalize() prior to this operation')
            return None
        try:  # in case closed with X
            id = self._TKCanvas2.create_text(converted_point[0], converted_point[1], text=text, font=font, fill=color,
                                             angle=angle)
        except:
            id = None
        return id

    def DrawImage(self, filename=None, data=None, location=(None, None), color='black', font=None, angle=0):
        """

        :param filename:  (Default value = None)
        :param data:  (Default value = None)
        :param location:  (Default value = (None, None))
        :param color:  (Default value = 'black')
        :param font: (common_key) specifies the font family, size, etc (Default value = None)
        :param angle:  (Default value = 0)

        """
        if location == (None, None):
            return
        if filename is not None:
            image = tk.PhotoImage(file=filename)
        elif data is not None:
            # if type(data) is bytes:
            try:
                image = tk.PhotoImage(data=data)
            except:
                return None  # an error likely means the window has closed so exit
        converted_point = self._convert_xy_to_canvas_xy(location[0], location[1])
        if self._TKCanvas2 is None:
            print('*** WARNING - The Graph element has not been finalized and cannot be drawn upon ***')
            print('Call Window.Finalize() prior to this operation')
            return None
        try:  # in case closed with X
            id = self._TKCanvas2.create_image(converted_point, image=image, anchor=tk.NW)
            self.Images[id] = image
        except:
            id = None
        return id

    def Erase(self):
        """ """
        if self._TKCanvas2 is None:
            print('*** WARNING - The Graph element has not been finalized and cannot be drawn upon ***')
            print('Call Window.Finalize() prior to this operation')
            return None
        self.Images = {}
        try:  # in case window was closed with X
            self._TKCanvas2.delete('all')
        except:
            pass

    def DeleteFigure(self, id):
        """

        :param id: 

        """
        try:
            self._TKCanvas2.delete(id)
        except:
            print('DeleteFigure - bad ID {}'.format(id))
        try:
            del self.Images[id]         # in case was an image. If wasn't an image, then will get exception
        except: pass

    def Update(self, background_color, visible=None):
        """

        :param background_color: color of background
        :param visible:  change visibility of element (Default value = None)

        """
        if self._TKCanvas2 is None:
            print('*** WARNING - The Graph element has not been finalized and cannot be drawn upon ***')
            print('Call Window.Finalize() prior to this operation')
            return None
        self._TKCanvas2.configure(background=background_color)
        if visible is False:
            self._TKCanvas2.pack_forget()
        elif visible is True:
            self._TKCanvas2.pack()

    def Move(self, x_direction, y_direction):
        """

        :param x_direction: 
        :param y_direction: 

        """
        zero_converted = self._convert_xy_to_canvas_xy(0, 0)
        shift_converted = self._convert_xy_to_canvas_xy(x_direction, y_direction)
        shift_amount = (shift_converted[0] - zero_converted[0], shift_converted[1] - zero_converted[1])
        if self._TKCanvas2 is None:
            print('*** WARNING - The Graph element has not been finalized and cannot be drawn upon ***')
            print('Call Window.Finalize() prior to this operation')
            return None
        self._TKCanvas2.move('all', shift_amount[0], shift_amount[1])

    def MoveFigure(self, figure, x_direction, y_direction):
        """

        :param figure: 
        :param x_direction: 
        :param y_direction: 

        """
        zero_converted = self._convert_xy_to_canvas_xy(0, 0)
        shift_converted = self._convert_xy_to_canvas_xy(x_direction, y_direction)
        shift_amount = (shift_converted[0] - zero_converted[0], shift_converted[1] - zero_converted[1])
        if figure is None:
            print('*** WARNING - Your figure is None. It most likely means your did not Finalize your Window ***')
            print('Call Window.Finalize() prior to all graph operations')
            return None
        self._TKCanvas2.move(figure, shift_amount[0], shift_amount[1])

    def RelocateFigure(self, figure, x, y):
        """

        :param figure: 
        :param x: 
        :param y: 

        """
        zero_converted = self._convert_xy_to_canvas_xy(0, 0)
        shift_converted = self._convert_xy_to_canvas_xy(x, y)
        shift_amount = (shift_converted[0] - zero_converted[0], shift_converted[1] - zero_converted[1])
        if figure is None:
            print('*** WARNING - Your figure is None. It most likely means your did not Finalize your Window ***')
            print('Call Window.Finalize() prior to all graph operations')
            return None
        xy = self._TKCanvas2.coords(figure)
        self._TKCanvas2.move(figure, shift_converted[0] - xy[0], shift_converted[1] - xy[1])

    @property
    def TKCanvas(self):
        """ """
        if self._TKCanvas2 is None:
            print('*** Did you forget to call Finalize()? Your code should look something like: ***')
            print('*** form = sg.Window("My Form").Layout(layout).Finalize() ***')
        return self._TKCanvas2

    # Realtime button release callback
    def ButtonReleaseCallBack(self, event):
        """

        :param event: 

        """
        self.ClickPosition = (None, None)
        self.LastButtonClickedWasRealtime = not self.DragSubmits
        if self.Key is not None:
            self.ParentForm.LastButtonClicked = self.Key
        else:
            self.ParentForm.LastButtonClicked = '__GRAPH__'  # need to put something rather than None
        if self.ParentForm.CurrentlyRunningMainloop:
            self.ParentForm.TKroot.quit()
        if self.DragSubmits:
            self.ParentForm.LastButtonClicked = None
        self.MouseButtonDown = False

    # Realtime button callback
    def ButtonPressCallBack(self, event):
        """

        :param event: 

        """
        self.ClickPosition = self._convert_canvas_xy_to_xy(event.x, event.y)
        self.ParentForm.LastButtonClickedWasRealtime = self.DragSubmits
        if self.Key is not None:
            self.ParentForm.LastButtonClicked = self.Key
        else:
            self.ParentForm.LastButtonClicked = '__GRAPH__'  # need to put something rather than None
        if self.ParentForm.CurrentlyRunningMainloop:
            self.ParentForm.TKroot.quit()  # kick out of loop if read was called
        self.MouseButtonDown = True

    # Realtime button callback
    def MotionCallBack(self, event):
        """

        :param event: 

        """
        if not self.MouseButtonDown:
            return
        self.ClickPosition = self._convert_canvas_xy_to_xy(event.x, event.y)
        self.ParentForm.LastButtonClickedWasRealtime = self.DragSubmits
        if self.Key is not None:
            self.ParentForm.LastButtonClicked = self.Key
        else:
            self.ParentForm.LastButtonClicked = '__GRAPH__'  # need to put something rather than None
        if self.ParentForm.CurrentlyRunningMainloop:
            self.ParentForm.TKroot.quit()  # kick out of loop if read was called

    def SetFocus(self):
        """ """
        self._TKCanvas2.focus_set()
        # self._TKCanvas2.focus_force()

    def __del__(self):
        """ """
        super().__del__()


# ---------------------------------------------------------------------- #
#                           Frame                                        #
# ---------------------------------------------------------------------- #
class Frame(Element):
    """ """
    
    def __init__(self, title, layout, title_color=None, background_color=None, title_location=None,
                 relief=DEFAULT_FRAME_RELIEF, size=(None, None), font=None, pad=None, border_width=None, key=None,
                 tooltip=None, right_click_menu=None, visible=True):
        """

        :param title: 
        :param layout: 
        :param title_color:  (Default value = None)
        :param background_color: color of background (Default value = None)
        :param title_location:  (Default value = None)
        :param relief:  (Default value = DEFAULT_FRAME_RELIEF)
        :param size: (common_key) (w,h) w=characters-wide, h=rows-high (Default value = (None, None))
        :param font: (common_key) specifies the font family, size, etc (Default value = None)
        :param pad: (common_key) Amount of padding to put around element (Default value = None)
        :param border_width:  (Default value = None)
        :param key: (common_key) Used with window.FindElement and with return values (Default value = None)
        :param tooltip: text, that will appear the you hover on (Default value = None)
        :param right_click_menu: see "Right Click Menus" (Default value = None)
        :param visible: set visibility state of the element (Default value = True)

        """
        
        self.UseDictionary = False
        self.ReturnValues = None
        self.ReturnValuesList = []
        self.ReturnValuesDictionary = {}
        self.DictionaryKeyCounter = 0
        self.ParentWindow = None
        self.Rows = []
        # self.ParentForm = None
        self.TKFrame = None
        self.Title = title
        self.Relief = relief
        self.TitleLocation = title_location
        self.BorderWidth = border_width
        self.BackgroundColor = background_color if background_color is not None else DEFAULT_BACKGROUND_COLOR
        self.RightClickMenu = right_click_menu
        self.ContainerElemementNumber = Window.GetAContainerNumber()

        self.Layout(layout)

        super().__init__(ELEM_TYPE_FRAME, background_color=background_color, text_color=title_color, size=size,
                         font=font, pad=pad, key=key, tooltip=tooltip, visible=visible)
        return

    def AddRow(self, *args):
        """Parms are a variable number of Elements

        :param *args: 

        """
        NumRows = len(self.Rows)  # number of existing rows is our row number
        CurrentRowNumber = NumRows  # this row's number
        CurrentRow = []  # start with a blank row and build up
        # -------------------------  Add the elements to a row  ------------------------- #
        for i, element in enumerate(args):  # Loop through list of elements and add them to the row
            element.Position = (CurrentRowNumber, i)
            element.ParentContainer = self
            CurrentRow.append(element)
            if element.Key is not None:
                self.UseDictionary = True
        # -------------------------  Append the row to list of Rows  ------------------------- #
        self.Rows.append(CurrentRow)

    def Layout(self, rows):
        """

        :param rows: 

        """
        for row in rows:
            self.AddRow(*row)

    def _GetElementAtLocation(self, location):
        """

        :param location: 

        """
        (row_num, col_num) = location
        row = self.Rows[row_num]
        element = row[col_num]
        return element

    def Update(self, visible=None):
        """

        :param visible:  change visibility of element (Default value = None)

        """
        
        if visible is False:
            self.TKFrame.pack_forget()
        elif visible is True:
            self.TKFrame.pack()

    def __del__(self):
        """ """
        for row in self.Rows:
            for element in row:
                element.__del__()
        super().__del__()


# ---------------------------------------------------------------------- #
#                           Separator                                    #
#  Routes stdout, stderr to a scrolled window                            #
# ---------------------------------------------------------------------- #
class VerticalSeparator(Element):
    """ """
    
    def __init__(self, pad=None):
        """

        :param pad: (common_key) Amount of padding to put around element (Default value = None)

        """
        
        self.Orientation = 'vertical'  # for now only vertical works

        super().__init__(ELEM_TYPE_SEPARATOR, pad=pad)

    def __del__(self):
        """ """
        super().__del__()


VSeperator = VerticalSeparator
VSep = VerticalSeparator


# ---------------------------------------------------------------------- #
#                           Tab                                          #
# ---------------------------------------------------------------------- #
class Tab(Element):
    """ """
    
    def __init__(self, title, layout, title_color=None, background_color=None, font=None, pad=None, disabled=False,
                 border_width=None, key=None, tooltip=None, right_click_menu=None, visible=True):
        """

        :param title: 
        :param layout: 
        :param title_color:  (Default value = None)
        :param background_color: color of background (Default value = None)
        :param font: (common_key) specifies the font family, size, etc (Default value = None)
        :param pad: (common_key) Amount of padding to put around element (Default value = None)
        :param disabled: set disable state for element (Default value = False)
        :param border_width:  (Default value = None)
        :param key: (common_key) Used with window.FindElement and with return values (Default value = None)
        :param tooltip: text, that will appear the you hover on (Default value = None)
        :param right_click_menu: see "Right Click Menus" (Default value = None)
        :param visible: set visibility state of the element (Default value = True)

        """
        
        self.UseDictionary = False
        self.ReturnValues = None
        self.ReturnValuesList = []
        self.ReturnValuesDictionary = {}
        self.DictionaryKeyCounter = 0
        self.ParentWindow = None
        self.Rows = []
        self.TKFrame = None
        self.Title = title
        self.BorderWidth = border_width
        self.Disabled = disabled
        self.ParentNotebook = None
        self.TabID = None
        self.BackgroundColor = background_color if background_color is not None else DEFAULT_BACKGROUND_COLOR
        self.RightClickMenu = right_click_menu
        self.ContainerElemementNumber = Window.GetAContainerNumber()

        self.Layout(layout)

        super().__init__(ELEM_TYPE_TAB, background_color=background_color, text_color=title_color, font=font, pad=pad,
                         key=key, tooltip=tooltip, visible=visible)
        return

    def AddRow(self, *args):
        """Parms are a variable number of Elements

        :param *args: 

        """
        NumRows = len(self.Rows)  # number of existing rows is our row number
        CurrentRowNumber = NumRows  # this row's number
        CurrentRow = []  # start with a blank row and build up
        # -------------------------  Add the elements to a row  ------------------------- #
        for i, element in enumerate(args):  # Loop through list of elements and add them to the row
            element.Position = (CurrentRowNumber, i)
            element.ParentContainer = self
            CurrentRow.append(element)
            if element.Key is not None:
                self.UseDictionary = True
        # -------------------------  Append the row to list of Rows  ------------------------- #
        self.Rows.append(CurrentRow)

    def Layout(self, rows):
        """

        :param rows: 

        """
        for row in rows:
            self.AddRow(*row)
        return self

    def Update(self, disabled=None, visible=None):  # TODO Disable / enable of tabs is not complete
        """

        :param disabled: disable or enable state of the element (Default value = None)
        :param visible:  change visibility of element (Default value = None)

        """
        
        if disabled is None:
            return
        self.Disabled = disabled
        state = 'disabled' if disabled is True else 'normal'
        self.ParentNotebook.tab(self.TabID, state=state)
        if visible is False:
            self.ParentNotebook.pack_forget()
        elif visible is True:
            self.ParentNotebook.pack()
        return self

    def _GetElementAtLocation(self, location):
        """

        :param location: 

        """
        (row_num, col_num) = location
        row = self.Rows[row_num]
        element = row[col_num]
        return element

    def __del__(self):
        """ """
        for row in self.Rows:
            for element in row:
                element.__del__()
        super().__del__()


# ---------------------------------------------------------------------- #
#                           TabGroup                                     #
# ---------------------------------------------------------------------- #
class TabGroup(Element):
    """ """
    
    def __init__(self, layout, tab_location=None, title_color=None, selected_title_color=None, background_color=None,
                 font=None, change_submits=False, enable_events=False, pad=None, border_width=None, theme=None,
                 key=None, tooltip=None, visible=True):
        """

        :param layout: 
        :param tab_location:  (Default value = None)
        :param title_color:  (Default value = None)
        :param selected_title_color:  (Default value = None)
        :param background_color: color of background (Default value = None)
        :param font: (common_key) specifies the font family, size, etc (Default value = None)
        :param change_submits: If True, pressing Enter key submits window (Default value = False)
        :param enable_events: Turns on the element specific events.(Default value = False)
        :param pad: (common_key) Amount of padding to put around element (Default value = None)
        :param border_width:  (Default value = None)
        :param theme:  (Default value = None)
        :param key: (common_key) Used with window.FindElement and with return values (Default value = None)
        :param tooltip: text, that will appear the you hover on (Default value = None)
        :param visible: set visibility state of the element (Default value = True)

        """
        
        self.UseDictionary = False
        self.ReturnValues = None
        self.ReturnValuesList = []
        self.ReturnValuesDictionary = {}
        self.DictionaryKeyCounter = 0
        self.ParentWindow = None
        self.SelectedTitleColor = selected_title_color
        self.Rows = []
        self.TKNotebook = None              # type: ttk.Notebook
        self.Widget = None                  # type: ttk.Notebook
        self.TabCount = 0
        self.BorderWidth = border_width
        self.Theme = theme
        self.BackgroundColor = background_color if background_color is not None else DEFAULT_BACKGROUND_COLOR
        self.ChangeSubmits = change_submits or enable_events
        self.TabLocation = tab_location

        self.Layout(layout)

        super().__init__(ELEM_TYPE_TAB_GROUP, background_color=background_color, text_color=title_color, font=font,
                         pad=pad, key=key, tooltip=tooltip, visible=visible)
        return

    def AddRow(self, *args):
        """Parms are a variable number of Elements

        :param *args: 

        """
        NumRows = len(self.Rows)  # number of existing rows is our row number
        CurrentRowNumber = NumRows  # this row's number
        CurrentRow = []  # start with a blank row and build up
        # -------------------------  Add the elements to a row  ------------------------- #
        for i, element in enumerate(args):  # Loop through list of elements and add them to the row
            element.Position = (CurrentRowNumber, i)
            element.ParentContainer = self
            CurrentRow.append(element)
            if element.Key is not None:
                self.UseDictionary = True
        # -------------------------  Append the row to list of Rows  ------------------------- #
        self.Rows.append(CurrentRow)

    def Layout(self, rows):
        """

        :param rows: 

        """
        for row in rows:
            self.AddRow(*row)

    def _GetElementAtLocation(self, location):
        """

        :param location: 

        """
        (row_num, col_num) = location
        row = self.Rows[row_num]
        element = row[col_num]
        return element

    def FindKeyFromTabName(self, tab_name):
        """

        :param tab_name: 

        """
        for row in self.Rows:
            for element in row:
                if element.Title == tab_name:
                    return element.Key
        return None

    def SelectTab(self, index):
        """

        :param index: 

        """
        try:
            self.TKNotebook.select(index)
        except Exception as e:
            print('Exception Selecting Tab {}'.format(e))

    def __del__(self):
        """ """
        for row in self.Rows:
            for element in row:
                element.__del__()
        super().__del__()


# ---------------------------------------------------------------------- #
#                           Slider                                       #
# ---------------------------------------------------------------------- #
class Slider(Element):
    """ """
    
    def __init__(self, range=(None, None), default_value=None, resolution=None, tick_interval=None, orientation=None,
                 disable_number_display=False, border_width=None, relief=None, change_submits=False,
                 enable_events=False, disabled=False, size=(None, None), font=None, background_color=None,
                 text_color=None, key=None, pad=None, tooltip=None, visible=True):
        """

        :param range:  (Default value = (None, None))
        :param default_value:  (Default value = None)
        :param resolution:  (Default value = None)
        :param tick_interval:  (Default value = None)
        :param orientation:  (Default value = None)
        :param disable_number_display:  (Default value = False)
        :param border_width:  (Default value = None)
        :param relief:  (Default value = None)
        :param change_submits: If True, pressing Enter key submits window (Default value = False)
        :param enable_events: Turns on the element specific events.(Default value = False)
        :param disabled: set disable state for element (Default value = False)
        :param size: (common_key) (w,h) w=characters-wide, h=rows-high (Default value = (None)
        :param font: (common_key) specifies the font family, size, etc (Default value = None)
        :param background_color: color of background (Default value = None)
        :param text_color: color of the text (Default value = None)
        :param key: (common_key) Used with window.FindElement and with return values (Default value = None)
        :param pad: (common_key) Amount of padding to put around element (Default value = None)
        :param tooltip: text, that will appear the you hover on (Default value = None)
        :param visible: set visibility state of the element (Default value = True)

        """
        
        self.TKScale = None  # type: tk.Scale
        self.Range = (1, 10) if range == (None, None) else range
        self.DefaultValue = self.Range[0] if default_value is None else default_value
        self.Orientation = orientation if orientation else DEFAULT_SLIDER_ORIENTATION
        self.BorderWidth = border_width if border_width else DEFAULT_SLIDER_BORDER_WIDTH
        self.Relief = relief if relief else DEFAULT_SLIDER_RELIEF
        self.Resolution = 1 if resolution is None else resolution
        self.ChangeSubmits = change_submits or enable_events
        self.Disabled = disabled
        self.TickInterval = tick_interval
        self.DisableNumericDisplay = disable_number_display
        temp_size = size
        if temp_size == (None, None):
            temp_size = (20, 20) if self.Orientation.startswith('h') else (8, 20)

        super().__init__(ELEM_TYPE_INPUT_SLIDER, size=temp_size, font=font, background_color=background_color,
                         text_color=text_color, key=key, pad=pad, tooltip=tooltip, visible=visible)
        return

    def Update(self, value=None, range=(None, None), disabled=None, visible=None):
        """

        :param value:  (Default value = None)
        :param range:  (Default value = (None, None))
        :param disabled: disable or enable state of the element (Default value = None)
        :param visible:  change visibility of element (Default value = None)

        """
        
        if value is not None:
            try:
                self.TKIntVar.set(value)
                if range != (None, None):
                    self.TKScale.config(from_=range[0], to_=range[1])
            except:
                pass
            self.DefaultValue = value
        if disabled == True:
            self.TKScale['state'] = 'disabled'
        elif disabled == False:
            self.TKScale['state'] = 'normal'
        if visible is False:
            self.TKScale.pack_forget()
        elif visible is True:
            self.TKScale.pack()

    def _SliderChangedHandler(self, event):
        """

        :param event: 

        """
        # first, get the results table built
        # modify the Results table in the parent FlexForm object
        if self.Key is not None:
            self.ParentForm.LastButtonClicked = self.Key
        else:
            self.ParentForm.LastButtonClicked = ''
        self.ParentForm.FormRemainedOpen = True
        if self.ParentForm.CurrentlyRunningMainloop:
            self.ParentForm.TKroot.quit()  # kick the users out of the mainloop

    def __del__(self):
        """ """
        super().__del__()


# ---------------------------------------------------------------------- #
#                          TkScrollableFrame (Used by Column)            #
# ---------------------------------------------------------------------- #
class TkFixedFrame(tk.Frame):
    """ """
    def __init__(self, master, **kwargs):
        """

        :param master: 
        :param **kwargs: 

        """
        tk.Frame.__init__(self, master, **kwargs)

        self.canvas = tk.Canvas(self)

        self.canvas.pack(side="left", fill="both", expand=True)

        # reset the view
        self.canvas.xview_moveto(0)
        self.canvas.yview_moveto(0)

        # create a frame inside the canvas which will be scrolled with it
        self.TKFrame = tk.Frame(self.canvas, **kwargs)
        self.frame_id = self.canvas.create_window(0, 0, window=self.TKFrame, anchor="nw")
        self.canvas.config(borderwidth=0, highlightthickness=0)
        self.TKFrame.config(borderwidth=0, highlightthickness=0)
        self.config(borderwidth=0, highlightthickness=0)


# ---------------------------------------------------------------------- #
#                          TkScrollableFrame (Used by Column)            #
# ---------------------------------------------------------------------- #
class TkScrollableFrame(tk.Frame):
    """ """
    def __init__(self, master, vertical_only, **kwargs):
        """

        :param master: 
        :param vertical_only: 
        :param **kwargs: 

        """
        tk.Frame.__init__(self, master, **kwargs)

        # create a canvas object and a vertical scrollbar for scrolling it
        self.vscrollbar = tk.Scrollbar(self, orient=tk.VERTICAL)
        self.vscrollbar.pack(side='right', fill="y", expand="false")

        if not vertical_only:
            self.hscrollbar = tk.Scrollbar(self, orient=tk.HORIZONTAL)
            self.hscrollbar.pack(side='bottom', fill="x", expand="false")
            self.canvas = tk.Canvas(self, yscrollcommand=self.vscrollbar.set, xscrollcommand=self.hscrollbar.set)
        else:
            self.canvas = tk.Canvas(self, yscrollcommand=self.vscrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)

        self.vscrollbar.config(command=self.canvas.yview)
        if not vertical_only:
            self.hscrollbar.config(command=self.canvas.xview)

        # reset the view
        self.canvas.xview_moveto(0)
        self.canvas.yview_moveto(0)

        # create a frame inside the canvas which will be scrolled with it
        self.TKFrame = tk.Frame(self.canvas, **kwargs)
        self.frame_id = self.canvas.create_window(0, 0, window=self.TKFrame, anchor="nw")
        self.canvas.config(borderwidth=0, highlightthickness=0)
        self.TKFrame.config(borderwidth=0, highlightthickness=0)
        self.config(borderwidth=0, highlightthickness=0)

        # scrollbar = tk.Scrollbar(frame)
        # scrollbar.pack(side=tk.RIGHT, fill='y')
        # scrollbar.config(command=treeview.yview)
        # self.vscrollbar.config(command=self.TKFrame.yview)
        # self.TKFrame.configure(yscrollcommand=self.vscrollbar.set)

        self.bind('<Configure>', self.set_scrollregion)

        self.bind_mouse_scroll(self.canvas, self.yscroll)
        if not vertical_only:
            self.bind_mouse_scroll(self.hscrollbar, self.xscroll)
        self.bind_mouse_scroll(self.vscrollbar, self.yscroll)

    def resize_frame(self, e):
        """

        :param e: 

        """
        self.canvas.itemconfig(self.frame_id, height=e.height, width=e.width)

    def yscroll(self, event):
        """

        :param event: 

        """
        if event.num == 5 or event.delta < 0:
            self.canvas.yview_scroll(1, "unit")
        elif event.num == 4 or event.delta > 0:
            self.canvas.yview_scroll(-1, "unit")

    def xscroll(self, event):
        """

        :param event: 

        """
        if event.num == 5 or event.delta < 0:
            self.canvas.xview_scroll(1, "unit")
        elif event.num == 4 or event.delta > 0:
            self.canvas.xview_scroll(-1, "unit")

    def bind_mouse_scroll(self, parent, mode):
        """

        :param parent: 
        :param mode: 

        """
        # ~~ Windows only
        parent.bind("<MouseWheel>", mode)
        # ~~ Unix only
        parent.bind("<Button-4>", mode)
        parent.bind("<Button-5>", mode)

    def set_scrollregion(self, event=None):
        """Set the scroll region on the canvas

        :param event:  (Default value = None)

        """
        self.canvas.configure(scrollregion=self.canvas.bbox('all'))


# ---------------------------------------------------------------------- #
#                           Column                                       #
# ---------------------------------------------------------------------- #
class Column(Element):
    """ """
    
    def __init__(self, layout, background_color=None, size=(None, None), pad=None, scrollable=False,
                 vertical_scroll_only=False, right_click_menu=None, key=None, visible=True):
        """

        :param layout: 
        :param background_color: color of background (Default value = None)
        :param size: (common_key) (w,h) w=characters-wide, h=rows-high (Default value = (None, None))
        :param pad: (common_key) Amount of padding to put around element (Default value = None)
        :param scrollable:  (Default value = False)
        :param vertical_scroll_only:  (Default value = False)
        :param right_click_menu: see "Right Click Menus" (Default value = None)
        :param key: (common_key) Used with window.FindElement and with return values (Default value = None)
        :param visible: set visibility state of the element (Default value = True)

        """
        
        self.UseDictionary = False
        self.ReturnValues = None
        self.ReturnValuesList = []
        self.ReturnValuesDictionary = {}
        self.DictionaryKeyCounter = 0
        self.ParentWindow = None
        self.ParentPanedWindow = None
        self.Rows = []
        self.TKFrame = None
        self.TKColFrame = None
        self.Scrollable = scrollable
        self.VerticalScrollOnly = vertical_scroll_only
        self.RightClickMenu = right_click_menu
        bg = background_color if background_color is not None else DEFAULT_BACKGROUND_COLOR
        self.ContainerElemementNumber = Window.GetAContainerNumber()

        self.Layout(layout)

        super().__init__(ELEM_TYPE_COLUMN, background_color=bg, size=size, pad=pad, key=key, visible=visible)
        return

    def AddRow(self, *args):
        """Parms are a variable number of Elements

        :param *args: 

        """
        NumRows = len(self.Rows)  # number of existing rows is our row number
        CurrentRowNumber = NumRows  # this row's number
        CurrentRow = []  # start with a blank row and build up
        # -------------------------  Add the elements to a row  ------------------------- #
        for i, element in enumerate(args):  # Loop through list of elements and add them to the row
            element.Position = (CurrentRowNumber, i)
            element.ParentContainer = self
            CurrentRow.append(element)
            if element.Key is not None:
                self.UseDictionary = True
        # -------------------------  Append the row to list of Rows  ------------------------- #
        self.Rows.append(CurrentRow)

    def Layout(self, rows):
        """

        :param rows: 

        """
        for row in rows:
            self.AddRow(*row)

    def _GetElementAtLocation(self, location):
        """

        :param location: 

        """
        (row_num, col_num) = location
        row = self.Rows[row_num]
        element = row[col_num]
        return element

    def Update(self, visible=None):
        """

        :param visible:  change visibility of element (Default value = None)

        """
        
        if visible is False:
            if self.TKColFrame:
                self.TKColFrame.pack_forget()
            if self.ParentPanedWindow:
                self.ParentPanedWindow.remove(self.TKColFrame)
        elif visible is True:
            if self.TKColFrame:
                self.TKColFrame.pack()
            if self.ParentPanedWindow:
                self.ParentPanedWindow.add(self.TKColFrame)

    def __del__(self):
        """ """
        for row in self.Rows:
            for element in row:
                element.__del__()
        try:
            del (self.TKFrame)
        except:
            pass
        super().__del__()


# ---------------------------------------------------------------------- #
#                           Pane                                       #
# ---------------------------------------------------------------------- #
class Pane(Element):
    """ """
    
    def __init__(self, pane_list, background_color=None, size=(None, None), pad=None, orientation='vertical',
                 show_handle=True, relief=RELIEF_RAISED, handle_size=None, border_width=None, key=None, visible=True):
        """

        :param pane_list: 
        :param background_color: color of background (Default value = None)
        :param size: (common_key) (w,h) w=characters-wide, h=rows-high (Default value = (None, None))
        :param pad: (common_key) Amount of padding to put around element (Default value = None)
        :param orientation:  (Default value = 'vertical')
        :param show_handle:  (Default value = True)
        :param relief:  (Default value = RELIEF_RAISED)
        :param handle_size:  (Default value = None)
        :param border_width:  (Default value = None)
        :param key: (common_key) Used with window.FindElement and with return values (Default value = None)
        :param visible: set visibility state of the element (Default value = True)

        """
        
        self.UseDictionary = False
        self.ReturnValues = None
        self.ReturnValuesList = []
        self.ReturnValuesDictionary = {}
        self.DictionaryKeyCounter = 0
        self.ParentWindow = None
        self.Rows = []
        self.TKFrame = None
        self.PanedWindow = None
        self.Orientation = orientation
        self.PaneList = pane_list
        self.ShowHandle = show_handle
        self.Relief = relief
        self.HandleSize = handle_size or 8
        self.BorderDepth = border_width
        bg = background_color if background_color is not None else DEFAULT_BACKGROUND_COLOR

        self.Rows = [pane_list]

        super().__init__(ELEM_TYPE_PANE, background_color=bg, size=size, pad=pad, key=key, visible=visible)
        return

    def Update(self, visible=None):
        """

        :param visible:  change visibility of element (Default value = None)

        """
        
        if visible is False:
            self.PanedWindow.pack_forget()
        elif visible is True:
            self.PanedWindow.pack()


# ---------------------------------------------------------------------- #
#                           Calendar                                     #
# ---------------------------------------------------------------------- #
class TKCalendar(ttk.Frame):
    """This code was shamelessly lifted from moshekaplan's repository - moshekaplan/tkinter_components"""
    # XXX ToDo: cget and configure

    datetime = calendar.datetime.datetime
    timedelta = calendar.datetime.timedelta

    def __init__(self, master=None, target_element=None, close_when_chosen=True, default_date=(None, None, None), **kw):
        """WIDGET-SPECIFIC OPTIONS
        
            locale, firstweekday, year, month, selectbackground,
            selectforeground

        :param master:  (Default value = None)
        :param target_element:  (Default value = None)
        :param close_when_chosen:  (Default value = True)
        :param default_date:  (Default value = (None)
        :param None:, None))
        :param **kw: 

        """
        self._TargetElement = target_element
        default_mon, default_day, default_year = default_date
        # remove custom options from kw before initializating ttk.Frame
        fwday = kw.pop('firstweekday', calendar.MONDAY)
        year = kw.pop('year', default_year or self.datetime.now().year)
        month = kw.pop('month', default_mon or self.datetime.now().month)
        locale = kw.pop('locale', None)
        sel_bg = kw.pop('selectbackground', '#ecffc4')
        sel_fg = kw.pop('selectforeground', '#05640e')
        self.format = kw.pop('format')
        if self.format is None:
            self.format = '%Y-%m-%d %H:%M:%S'

        self._date = self.datetime(year, month, default_day or 1)
        self._selection = None  # no date selected
        self._master = master
        self.close_when_chosen = close_when_chosen
        ttk.Frame.__init__(self, master, **kw)

        # instantiate proper calendar class
        if locale is None:
            self._cal = calendar.TextCalendar(fwday)
        else:
            self._cal = calendar.LocaleTextCalendar(fwday, locale)

        self.__setup_styles()  # creates custom styles
        self.__place_widgets()  # pack/grid used widgets
        self.__config_calendar()  # adjust calendar columns and setup tags
        # configure a canvas, and proper bindings, for selecting dates
        self.__setup_selection(sel_bg, sel_fg)

        # store items ids, used for insertion later
        self._items = [self._calendar.insert('', 'end', values='')
                       for _ in range(6)]
        # insert dates in the currently empty calendar
        self._build_calendar()

    def __setitem__(self, item, value):
        """

        :param item: 
        :param value: 

        """
        if item in ('year', 'month'):
            raise AttributeError("attribute '%s' is not writeable" % item)
        elif item == 'selectbackground':
            self._canvas['background'] = value
        elif item == 'selectforeground':
            self._canvas.itemconfigure(self._canvas.text, item=value)
        else:
            ttk.Frame.__setitem__(self, item, value)

    def __getitem__(self, item):
        """

        :param item: 

        """
        if item in ('year', 'month'):
            return getattr(self._date, item)
        elif item == 'selectbackground':
            return self._canvas['background']
        elif item == 'selectforeground':
            return self._canvas.itemcget(self._canvas.text, 'fill')
        else:
            r = ttk.tclobjs_to_py({item: ttk.Frame.__getitem__(self, item)})
            return r[item]

    def __setup_styles(self):
        """ """
        # custom ttk styles
        style = ttk.Style(self.master)
        arrow_layout = lambda dir: (
            [('Button.focus', {'children': [('Button.%sarrow' % dir, None)]})]
        )
        style.layout('L.TButton', arrow_layout('left'))
        style.layout('R.TButton', arrow_layout('right'))

    def __place_widgets(self):
        """ """
        # header frame and its widgets
        hframe = ttk.Frame(self)
        lbtn = ttk.Button(hframe, style='L.TButton', command=self._prev_month)
        rbtn = ttk.Button(hframe, style='R.TButton', command=self._next_month)
        self._header = ttk.Label(hframe, width=15, anchor='center')
        # the calendar
        self._calendar = ttk.Treeview(self, show='', selectmode='none', height=7)

        # pack the widgets
        hframe.pack(in_=self, side='top', pady=4, anchor='center')
        lbtn.grid(in_=hframe)
        self._header.grid(in_=hframe, column=1, row=0, padx=12)
        rbtn.grid(in_=hframe, column=2, row=0)
        self._calendar.pack(in_=self, expand=1, fill='both', side='bottom')

    def __config_calendar(self):
        """ """
        cols = self._cal.formatweekheader(3).split()
        self._calendar['columns'] = cols
        self._calendar.tag_configure('header', background='grey90')
        self._calendar.insert('', 'end', values=cols, tag='header')
        # adjust its columns width
        font = tkinter.font.Font()
        maxwidth = max(font.measure(col) for col in cols)
        for col in cols:
            self._calendar.column(col, width=maxwidth, minwidth=maxwidth,
                                  anchor='e')

    def __setup_selection(self, sel_bg, sel_fg):
        """

        :param sel_bg: 
        :param sel_fg: 

        """
        self._font = tkinter.font.Font()
        self._canvas = canvas = tk.Canvas(self._calendar,
                                          background=sel_bg, borderwidth=0, highlightthickness=0)
        canvas.text = canvas.create_text(0, 0, fill=sel_fg, anchor='w')

        canvas.bind('<ButtonPress-1>', lambda evt: canvas.place_forget())
        self._calendar.bind('<Configure>', lambda evt: canvas.place_forget())
        self._calendar.bind('<ButtonPress-1>', self._pressed)

    def __minsize(self, evt):
        """

        :param evt: 

        """
        width, height = self._calendar.master.geometry().split('x')
        height = height[:height.index('+')]
        self._calendar.master.minsize(width, height)

    def _build_calendar(self):
        """ """
        year, month = self._date.year, self._date.month

        # update header text (Month, YEAR)
        header = self._cal.formatmonthname(year, month, 0)
        self._header['text'] = header.title()

        # update calendar shown dates
        cal = self._cal.monthdayscalendar(year, month)
        for indx, item in enumerate(self._items):
            week = cal[indx] if indx < len(cal) else []
            fmt_week = [('%02d' % day) if day else '' for day in week]
            self._calendar.item(item, values=fmt_week)

    def _show_selection(self, text, bbox):
        """Configure canvas for a new selection.

        :param text: 
        :param bbox: 

        """
        x, y, width, height = bbox

        textw = self._font.measure(text)

        canvas = self._canvas
        canvas.configure(width=width, height=height)
        canvas.coords(canvas.text, width - textw, height / 2 - 1)
        canvas.itemconfigure(canvas.text, text=text)
        canvas.place(in_=self._calendar, x=x, y=y)

    # Callbacks

    def _pressed(self, evt):
        """Clicked somewhere in the calendar.

        :param evt: 

        """
        x, y, widget = evt.x, evt.y, evt.widget
        item = widget.identify_row(y)
        column = widget.identify_column(x)

        if not column or not item in self._items:
            # clicked in the weekdays row or just outside the columns
            return

        item_values = widget.item(item)['values']
        if not len(item_values):  # row is empty for this month
            return

        text = item_values[int(column[1]) - 1]
        if not text:  # date is empty
            return

        bbox = widget.bbox(item, column)
        if not bbox:  # calendar not visible yet
            return

        # update and then show selection
        text = '%02d' % text
        self._selection = (text, item, column)
        self._show_selection(text, bbox)
        year, month = self._date.year, self._date.month
        now = self.datetime.now()
        try:
            self._TargetElement.Update(
                self.datetime(year, month, int(self._selection[0]), now.hour, now.minute, now.second).strftime(
                    self.format))
            if self._TargetElement.ChangeSubmits:
                self._TargetElement.ParentForm.LastButtonClicked = self._TargetElement.Key
                self._TargetElement.ParentForm.FormRemainedOpen = True
                self._TargetElement.ParentForm.TKroot.quit()  # kick the users out of the mainloop
        except:
            pass
        if self.close_when_chosen:
            self._master.destroy()

    def _prev_month(self):
        """Updated calendar to show the previous month."""
        self._canvas.place_forget()

        self._date = self._date - self.timedelta(days=1)
        self._date = self.datetime(self._date.year, self._date.month, 1)
        self._build_calendar()  # reconstuct calendar

    def _next_month(self):
        """Update calendar to show the next month."""
        self._canvas.place_forget()

        year, month = self._date.year, self._date.month
        self._date = self._date + self.timedelta(
            days=calendar.monthrange(year, month)[1] + 1)
        self._date = self.datetime(self._date.year, self._date.month, 1)
        self._build_calendar()  # reconstruct calendar

    # Properties

    @property
    def selection(self):
        """ """
        if not self._selection:
            return None

        year, month = self._date.year, self._date.month
        return self.datetime(year, month, int(self._selection[0]))


# ---------------------------------------------------------------------- #
#                           Menu                                       #
# ---------------------------------------------------------------------- #
class Menu(Element):
    """ """
    
    def __init__(self, menu_definition, background_color=None, size=(None, None), tearoff=False, pad=None, key=None,
                 visible=True):
        """

        :param menu_definition: 
        :param background_color: color of background (Default value = None)
        :param size: (common_key) (w,h) w=characters-wide, h=rows-high (Default value = (None, None))
        :param tearoff:  (Default value = False)
        :param pad: (common_key) Amount of padding to put around element (Default value = None)
        :param key: (common_key) Used with window.FindElement and with return values (Default value = None)
        :param visible: set visibility state of the element (Default value = True)

        """
        
        self.BackgroundColor = background_color if background_color is not None else DEFAULT_BACKGROUND_COLOR
        self.MenuDefinition = menu_definition
        self.TKMenu = None                  # type: tk.Menu
        self.Tearoff = tearoff
        self.MenuItemChosen = None

        super().__init__(ELEM_TYPE_MENUBAR, background_color=background_color, size=size, pad=pad, key=key,
                         visible=visible)
        return

    def _MenuItemChosenCallback(self, item_chosen):  # Menu Menu Item Chosen Callback
        """

        :param item_chosen: 

        """
        # print('IN MENU ITEM CALLBACK', item_chosen)
        self.MenuItemChosen = item_chosen
        self.ParentForm.LastButtonClicked = item_chosen
        self.ParentForm.FormRemainedOpen = True
        if self.ParentForm.CurrentlyRunningMainloop:
            self.ParentForm.TKroot.quit()  # kick the users out of the mainloop

    def Update(self, menu_definition, visible=None):
        """

        :param menu_definition: 
        :param visible:  change visibility of element (Default value = None)

        """
        
        self.MenuDefinition = menu_definition
        self.TKMenu = tk.Menu(self.ParentForm.TKroot, tearoff=self.Tearoff)  # create the menubar
        menubar = self.TKMenu
        for menu_entry in menu_definition:
            # print(f'Adding a Menubar ENTRY {menu_entry}')
            baritem = tk.Menu(menubar, tearoff=self.Tearoff)
            pos = menu_entry[0].find('&')
            # print(pos)
            if pos != -1:
                if pos == 0 or menu_entry[0][pos - 1] != "\\":
                    menu_entry[0] = menu_entry[0][:pos] + menu_entry[0][pos + 1:]
            if menu_entry[0][0] == MENU_DISABLED_CHARACTER:
                menubar.add_cascade(label=menu_entry[0][len(MENU_DISABLED_CHARACTER):], menu=baritem, underline=pos)
                menubar.entryconfig(menu_entry[0][len(MENU_DISABLED_CHARACTER):], state='disabled')
            else:
                menubar.add_cascade(label=menu_entry[0], menu=baritem, underline=pos)

            if len(menu_entry) > 1:
                AddMenuItem(baritem, menu_entry[1], self)
        self.ParentForm.TKroot.configure(menu=self.TKMenu)
        # TODO add visible code for menus

    def __del__(self):
        """ """
        super().__del__()


MenuBar = Menu  # another name for Menu to make it clear it's the Menu Bar


# ---------------------------------------------------------------------- #
#                           Table                                        #
# ---------------------------------------------------------------------- #
class Table(Element):
    """ """
    
    def __init__(self, values, headings=None, visible_column_map=None, col_widths=None, def_col_width=10,
                 auto_size_columns=True, max_col_width=20, select_mode=None, display_row_numbers=False, num_rows=None,
                 row_height=None, font=None, justification='right', text_color=None, background_color=None,
                 alternating_row_color=None, row_colors=None, vertical_scroll_only=True, hide_vertical_scroll=False,
                 size=(None, None), change_submits=False, enable_events=False, bind_return_key=False, pad=None,
                 key=None, tooltip=None, right_click_menu=None, visible=True):
        """

        :param values: 
        :param headings:  (Default value = None)
        :param visible_column_map:  (Default value = None)
        :param col_widths:  (Default value = None)
        :param def_col_width:  (Default value = 10)
        :param auto_size_columns:  (Default value = True)
        :param max_col_width:  (Default value = 20)
        :param select_mode:  (Default value = None)
        :param display_row_numbers:  (Default value = False)
        :param num_rows:  (Default value = None)
        :param row_height:  (Default value = None)
        :param font: (common_key) specifies the font family, size, etc (Default value = None)
        :param justification:  (Default value = 'right')
        :param text_color: color of the text (Default value = None)
        :param background_color: color of background (Default value = None)
        :param alternating_row_color:  (Default value = None)
        :param row_colors:  (Default value = None)
        :param vertical_scroll_only:  (Default value = True)
        :param hide_vertical_scroll:  (Default value = False)
        :param size: (common_key) (w,h) w=characters-wide, h=rows-high (Default value = (None, None))
        :param change_submits: If True, pressing Enter key submits window (Default value = False)
        :param enable_events: Turns on the element specific events.(Default value = False)
        :param bind_return_key:  (Default value = False)
        :param pad: (common_key) Amount of padding to put around element (Default value = None)
        :param key: (common_key) Used with window.FindElement and with return values (Default value = None)
        :param tooltip: text, that will appear the you hover on (Default value = None)
        :param right_click_menu: see "Right Click Menus" (Default value = None)
        :param visible: set visibility state of the element (Default value = True)

        """
        
        self.Values = values
        self.ColumnHeadings = headings
        self.ColumnsToDisplay = visible_column_map
        self.ColumnWidths = col_widths
        self.MaxColumnWidth = max_col_width
        self.DefaultColumnWidth = def_col_width
        self.AutoSizeColumns = auto_size_columns
        self.BackgroundColor = background_color if background_color is not None else DEFAULT_BACKGROUND_COLOR
        self.TextColor = text_color
        self.Justification = justification
        self.InitialState = None
        self.SelectMode = select_mode
        self.DisplayRowNumbers = display_row_numbers
        self.NumRows = num_rows if num_rows is not None else size[1]
        self.RowHeight = row_height
        self.TKTreeview = None                      # type: ttk.Treeview
        self.AlternatingRowColor = alternating_row_color
        self.VerticalScrollOnly = vertical_scroll_only
        self.HideVerticalScroll = hide_vertical_scroll
        self.SelectedRows = []
        self.ChangeSubmits = change_submits or enable_events
        self.BindReturnKey = bind_return_key
        self.StartingRowNumber = 0  # When displaying row numbers, where to start
        self.RowHeaderText = 'Row'
        self.RightClickMenu = right_click_menu
        self.RowColors = row_colors

        super().__init__(ELEM_TYPE_TABLE, text_color=text_color, background_color=background_color, font=font,
                         size=size, pad=pad, key=key, tooltip=tooltip, visible=visible)
        return

    def Update(self, values=None, num_rows=None, visible=None, select_rows=None):
        """

        :param values:  (Default value = None)
        :param num_rows:  (Default value = None)
        :param visible:  change visibility of element (Default value = None)
        :param select_rows:  (Default value = None)

        """
        
        if values is not None:
            children = self.TKTreeview.get_children()
            for i in children:
                self.TKTreeview.detach(i)
                self.TKTreeview.delete(i)
            children = self.TKTreeview.get_children()
            # self.TKTreeview.delete(*self.TKTreeview.get_children())
            for i, value in enumerate(values):
                if self.DisplayRowNumbers:
                    value = [i + self.StartingRowNumber] + value
                id = self.TKTreeview.insert('', 'end', text=i, iid=i + 1, values=value, tag=i % 2)
            if self.AlternatingRowColor is not None:
                self.TKTreeview.tag_configure(1, background=self.AlternatingRowColor)
            self.Values = values
            self.SelectedRows = []
        if visible is False:
            self.TKTreeview.pack_forget()
        elif visible is True:
            self.TKTreeview.pack()
        if num_rows is not None:
            self.TKTreeview.config(height=num_rows)
        if select_rows is not None:
            rows_to_select = [i+1 for i in select_rows]
            self.TKTreeview.selection_set(rows_to_select)

    def treeview_selected(self, event):
        """

        :param event: 

        """
        selections = self.TKTreeview.selection()
        self.SelectedRows = [int(x) - 1 for x in selections]
        if self.ChangeSubmits:
            MyForm = self.ParentForm
            if self.Key is not None:
                self.ParentForm.LastButtonClicked = self.Key
            else:
                self.ParentForm.LastButtonClicked = ''
            self.ParentForm.FormRemainedOpen = True
            if self.ParentForm.CurrentlyRunningMainloop:
                self.ParentForm.TKroot.quit()

    def treeview_double_click(self, event):
        """

        :param event: 

        """
        selections = self.TKTreeview.selection()
        self.SelectedRows = [int(x) - 1 for x in selections]
        if self.BindReturnKey:
            MyForm = self.ParentForm
            if self.Key is not None:
                self.ParentForm.LastButtonClicked = self.Key
            else:
                self.ParentForm.LastButtonClicked = ''
            self.ParentForm.FormRemainedOpen = True
            if self.ParentForm.CurrentlyRunningMainloop:
                self.ParentForm.TKroot.quit()

    def __del__(self):
        """ """
        super().__del__()


# ---------------------------------------------------------------------- #
#                           Tree                                         #
# ---------------------------------------------------------------------- #
class Tree(Element):
    """ """
    
    def __init__(self, data=None, headings=None, visible_column_map=None, col_widths=None, col0_width=10,
                 def_col_width=10, auto_size_columns=True, max_col_width=20, select_mode=None, show_expanded=False,
                 change_submits=False, enable_events=False, font=None, justification='right', text_color=None,
                 background_color=None, num_rows=None, row_height=None, pad=None, key=None, tooltip=None,
                 right_click_menu=None, visible=True):
        """

        :param data:  (Default value = None)
        :param headings:  (Default value = None)
        :param visible_column_map:  (Default value = None)
        :param col_widths:  (Default value = None)
        :param col0_width:  (Default value = 10)
        :param def_col_width:  (Default value = 10)
        :param auto_size_columns:  (Default value = True)
        :param max_col_width:  (Default value = 20)
        :param select_mode:  (Default value = None)
        :param show_expanded:  (Default value = False)
        :param change_submits: If True, pressing Enter key submits window (Default value = False)
        :param enable_events: Turns on the element specific events.(Default value = False)
        :param font: (common_key) specifies the font family, size, etc (Default value = None)
        :param justification:  (Default value = 'right')
        :param text_color: color of the text (Default value = None)
        :param background_color: color of background (Default value = None)
        :param num_rows:  (Default value = None)
        :param row_height:  (Default value = None)
        :param pad: (common_key) Amount of padding to put around element (Default value = None)
        :param key: (common_key) Used with window.FindElement and with return values (Default value = None)
        :param tooltip: text, that will appear the you hover on (Default value = None)
        :param right_click_menu: see "Right Click Menus" (Default value = None)
        :param visible: set visibility state of the element (Default value = True)

        """
        
        self.TreeData = data
        self.ColumnHeadings = headings
        self.ColumnsToDisplay = visible_column_map
        self.ColumnWidths = col_widths
        self.MaxColumnWidth = max_col_width
        self.DefaultColumnWidth = def_col_width
        self.AutoSizeColumns = auto_size_columns
        self.BackgroundColor = background_color if background_color is not None else DEFAULT_BACKGROUND_COLOR
        self.TextColor = text_color
        self.Justification = justification
        self.InitialState = None
        self.SelectMode = select_mode
        self.ShowExpanded = show_expanded
        self.NumRows = num_rows
        self.Col0Width = col0_width
        self.TKTreeview = None
        self.SelectedRows = []
        self.ChangeSubmits = change_submits or enable_events
        self.RightClickMenu = right_click_menu
        self.RowHeight = row_height
        self.IconList = {}

        super().__init__(ELEM_TYPE_TREE, text_color=text_color, background_color=background_color, font=font, pad=pad,
                         key=key, tooltip=tooltip, visible=visible)
        return

    def treeview_selected(self, event):
        """

        :param event: 

        """
        selections = self.TKTreeview.selection()
        self.SelectedRows = [x for x in selections]
        if self.ChangeSubmits:
            MyForm = self.ParentForm
            if self.Key is not None:
                self.ParentForm.LastButtonClicked = self.Key
            else:
                self.ParentForm.LastButtonClicked = ''
            self.ParentForm.FormRemainedOpen = True
            if self.ParentForm.CurrentlyRunningMainloop:
                self.ParentForm.TKroot.quit()

    def add_treeview_data(self, node):
        """

        :param node: 

        """
        # print(f'Inserting {node.key} under parent {node.parent}')
        if node.key != '':
            if node.icon:
                try:
                    if type(node.icon) is bytes:
                        photo = tk.PhotoImage(data=node.icon)
                    else:
                        photo = tk.PhotoImage(file=node.icon)
                    node.photo = photo
                    self.TKTreeview.insert(node.parent, 'end', node.key, text=node.text, values=node.values,
                                           open=self.ShowExpanded, image=node.photo)
                except:
                    self.photo = None
            else:
                self.TKTreeview.insert(node.parent, 'end', node.key, text=node.text, values=node.values,
                                       open=self.ShowExpanded)

        for node in node.children:
            self.add_treeview_data(node)

    def Update(self, values=None, key=None, value=None, text=None, icon=None, visible=None):
        """

        :param values:  (Default value = None)
        :param key: (common_key) Used with window.FindElement and with return values (Default value = None)
        :param value:  (Default value = None)
        :param text:  (Default value = None)
        :param icon:  (Default value = None)
        :param visible:  change visibility of element (Default value = None)

        """
        
        if values is not None:
            children = self.TKTreeview.get_children()
            for i in children:
                self.TKTreeview.detach(i)
                self.TKTreeview.delete(i)
            children = self.TKTreeview.get_children()
            self.TreeData = values
            self.add_treeview_data(self.TreeData.root_node)
            self.SelectedRows = []
        if key is not None:
            item = self.TKTreeview.item(key)
            if value is not None:
                self.TKTreeview.item(key, values=value)
            if text is not None:
                self.TKTreeview.item(key, text=text)
            if icon is not None:
                try:
                    if type(icon) is bytes:
                        photo = tk.PhotoImage(data=icon)
                    else:
                        photo = tk.PhotoImage(file=icon)
                    self.TKTreeview.item(key, image=photo)
                    self.IconList[key] = photo  # save so that it's not deleted (save reference)
                except:
                    pass
            item = self.TKTreeview.item(key)
        if visible is False:
            self.TKTreeview.pack_forget()
        elif visible is True:
            self.TKTreeview.pack()
        return self

    def __del__(self):
        """ """
        super().__del__()


class TreeData(object):
    """ """
    class Node(object):
        """ """
        def __init__(self, parent, key, text, values, icon=None):
            """

            :param parent: 
            :param key: (common_key) Used with window.FindElement and with return values
            :param text: 
            :param values: 
            :param icon:  (Default value = None)

            """
            self.parent = parent
            self.children = []
            self.key = key
            self.text = text
            self.values = values
            self.icon = icon

        def _Add(self, node):
            """

            :param node: 

            """
            self.children.append(node)

    def __init__(self):
        """ """
        self.tree_dict = {}
        self.root_node = self.Node("", "", 'root', [], None)
        self.tree_dict[""] = self.root_node

    def _AddNode(self, key, node):
        """

        :param key: (common_key) Used with window.FindElement and with return values
        :param node: 

        """
        self.tree_dict[key] = node

    def Insert(self, parent, key, text, values, icon=None):
        """

        :param parent: 
        :param key: (common_key) Used with window.FindElement and with return values
        :param text: 
        :param values: 
        :param icon:  (Default value = None)

        """
        node = self.Node(parent, key, text, values, icon)
        self.tree_dict[key] = node
        parent_node = self.tree_dict[parent]
        parent_node._Add(node)

    def __repr__(self):
        """ """
        return self._NodeStr(self.root_node, 1)

    def _NodeStr(self, node, level):
        """

        :param node: 
        :param level: 

        """
        return '\n'.join(
            [str(node.key) + ' : ' + str(node.text)] +
            [' ' * 4 * level + self._NodeStr(child, level + 1) for child in node.children])


# ---------------------------------------------------------------------- #
#                           Error Element                                #
# ---------------------------------------------------------------------- #
class ErrorElement(Element):
    """ """
    def __init__(self, key=None):
        """Error Element

        :param key: (common_key) Used with window.FindElement and with return values (Default value = None)

        """
        self.Key = key

        super().__init__(ELEM_TYPE_ERROR, key=key)
        return

    def Update(self, silent_on_error=True, *args, **kwargs):
        """

        :param silent_on_error:  (Default value = True)
        :param *args: 
        :param **kwargs: 

        """
        if not silent_on_error:
            PopupError('Keyword error in Update',
                       'You need to stop this madness and check your spelling',
                       'Bad key = {}'.format(self.Key),
                       'Your bad line of code may resemble this:',
                       'window.FindElement("{}")'.format(self.Key))
        return self

    def Get(self):
        """ """
        return 'This is NOT a valid Element!\nSTOP trying to do things with it or I will have to crash at some point!'

    def __del__(self):
        """ """
        super().__del__()


# ---------------------------------------------------------------------- #
#                           Stretch Element                              #
# ---------------------------------------------------------------------- #
# This is for source code compatibility with tkinter version. No tkinter equivalent
Stretch = ErrorElement


# ------------------------------------------------------------------------- #
#                       Window CLASS                                        #
# ------------------------------------------------------------------------- #
class Window:
    """ """
    
    NumOpenWindows = 0
    user_defined_icon = None
    hidden_master_root = None
    animated_popup_dict = {}
    container_element_counter = 0  # used to get a number of Container Elements (Frame, Column, Tab)
    read_call_from_debugger = False

    def __init__(self, title, layout=None, default_element_size=DEFAULT_ELEMENT_SIZE,
                 default_button_element_size=(None, None),
                 auto_size_text=None, auto_size_buttons=None, location=(None, None), size=(None, None),
                 element_padding=None, margins=(None, None), button_color=None, font=None,
                 progress_bar_color=(None, None), background_color=None, border_depth=None, auto_close=False,
                 auto_close_duration=DEFAULT_AUTOCLOSE_TIME, icon=DEFAULT_WINDOW_ICON, force_toplevel=False,
                 alpha_channel=1, return_keyboard_events=False, use_default_focus=True, text_justification=None,
                 no_titlebar=False, grab_anywhere=False, keep_on_top=False, resizable=False, disable_close=False,
                 disable_minimize=False, right_click_menu=None, transparent_color=None, debugger_enabled=True):
        """

        :param title: 
        :param layout:  (Default value = None)
        :param default_element_size:  (Default value = DEFAULT_ELEMENT_SIZE)
        :param default_button_element_size:  (Default value = (None, None))
        :param auto_size_text: True if size should fit the text length (Default value = None)
        :param auto_size_buttons:  (Default value = None)
        :param location:  (Default value = (None)
        :param size: (common_key) (w,h) w=characters-wide, h=rows-high (Default value = (None)
        :param element_padding:  (Default value = None)
        :param margins:  (Default value = (None)
        :param button_color:  (Default value = None)
        :param font: (common_key) specifies the font family, size, etc (Default value = None)
        :param progress_bar_color:  (Default value = (None)
        :param background_color: color of background (Default value = None)
        :param border_depth:  (Default value = None)
        :param auto_close:  (Default value = False)
        :param auto_close_duration:  (Default value = DEFAULT_AUTOCLOSE_TIME)
        :param icon: Icon to display (Default value = DEFAULT_WINDOW_ICON)
        :param force_toplevel:  (Default value = False)
        :param alpha_channel:  (Default value = 1)
        :param return_keyboard_events:  (Default value = False)
        :param use_default_focus:  (Default value = True)
        :param text_justification:  (Default value = None)
        :param no_titlebar:  (Default value = False)
        :param grab_anywhere: If True can grab anywhere to move the window (Default value = False)
        :param location: Location on screen to display (Default value = (None, None))
        :param resizable:  (Default value = False)
        :param disable_close:  (Default value = False)
        :param disable_minimize:  (Default value = False)
        :param right_click_menu: see "Right Click Menus" (Default value = None)
        :param transparent_color:  (Default value = None)
        :param debugger_enabled:  (Default value = True)

        """
        
        self.AutoSizeText = auto_size_text if auto_size_text is not None else DEFAULT_AUTOSIZE_TEXT
        self.AutoSizeButtons = auto_size_buttons if auto_size_buttons is not None else DEFAULT_AUTOSIZE_BUTTONS
        self.Title = title
        self.Rows = []  # a list of ELEMENTS for this row
        self.DefaultElementSize = default_element_size
        self.DefaultButtonElementSize = default_button_element_size if default_button_element_size != (
            None, None) else DEFAULT_BUTTON_ELEMENT_SIZE
        self.Location = location
        self.ButtonColor = button_color if button_color else DEFAULT_BUTTON_COLOR
        self.BackgroundColor = background_color if background_color else DEFAULT_BACKGROUND_COLOR
        self.ParentWindow = None
        self.Font = font if font else DEFAULT_FONT
        self.RadioDict = {}
        self.BorderDepth = border_depth
        self.WindowIcon = Window.user_defined_icon if Window.user_defined_icon is not None else icon if icon is not None else DEFAULT_WINDOW_ICON
        self.AutoClose = auto_close
        self.NonBlocking = False
        self.TKroot = None
        self.TKrootDestroyed = False
        self.CurrentlyRunningMainloop = False
        self.FormRemainedOpen = False
        self.TKAfterID = None
        self.ProgressBarColor = progress_bar_color
        self.AutoCloseDuration = auto_close_duration
        self.RootNeedsDestroying = False
        self.Shown = False
        self.ReturnValues = None
        self.ReturnValuesList = []
        self.ReturnValuesDictionary = {}
        self.DictionaryKeyCounter = 0
        self.LastButtonClicked = None
        self.LastButtonClickedWasRealtime = False
        self.UseDictionary = False
        self.UseDefaultFocus = use_default_focus
        self.ReturnKeyboardEvents = return_keyboard_events
        self.LastKeyboardEvent = None
        self.TextJustification = text_justification
        self.NoTitleBar = no_titlebar
        self.GrabAnywhere = grab_anywhere
        self.KeepOnTop = keep_on_top
        self.ForceTopLevel = force_toplevel
        self.Resizable = resizable
        self._AlphaChannel = alpha_channel
        self.Timeout = None
        self.TimeoutKey = '_timeout_'
        self.TimerCancelled = False
        self.DisableClose = disable_close
        self.DisableMinimize = disable_minimize
        self._Hidden = False
        self._Size = size
        self.XFound = False
        self.ElementPadding = element_padding or DEFAULT_ELEMENT_PADDING
        self.RightClickMenu = right_click_menu
        self.Margins = margins if margins != (None, None) else DEFAULT_MARGINS
        self.ContainerElemementNumber = Window.GetAContainerNumber()
        self.AllKeysDict = {}
        self.TransparentColor = transparent_color
        self.UniqueKeyCounter = 0
        self.DebuggerEnabled = debugger_enabled
        if layout is not None:
            self.Layout(layout)

    @classmethod
    def GetAContainerNumber(cls):
        """ """
        cls.container_element_counter += 1
        return cls.container_element_counter

    @classmethod
    def IncrementOpenCount(self):
        """ """
        self.NumOpenWindows += 1
        # print('+++++ INCREMENTING Num Open Windows = {} ---'.format(Window.NumOpenWindows))

    @classmethod
    def DecrementOpenCount(self):
        """ """
        self.NumOpenWindows -= 1 * (self.NumOpenWindows != 0)  # decrement if not 0
        # print('----- DECREMENTING Num Open Windows = {} ---'.format(Window.NumOpenWindows))

    # ------------------------- Add ONE Row to Form ------------------------- #
    def AddRow(self, *args):
        """Parms are a variable number of Elements

        :param *args: 

        """
        NumRows = len(self.Rows)  # number of existing rows is our row number
        CurrentRowNumber = NumRows  # this row's number
        CurrentRow = []  # start with a blank row and build up
        # -------------------------  Add the elements to a row  ------------------------- #
        for i, element in enumerate(args):  # Loop through list of elements and add them to the row
            if type(element) == list:
                PopupError('Error creating layout',
                      'Layout has a LIST instead of an ELEMENT',
                      'This means you have a badly placed ]',
                      'The offensive list is:',
                      element,
                      'This list will be stripped from your layout'
                      )
                continue
            elif callable(element):
                PopupError('Error creating layout',
                      'Layout has a FUNCTION instead of an ELEMENT',
                      'This means you are missing () from your layout',
                      'The offensive list is:',
                      element,
                      'This item will be stripped from your layout'
                      )
                continue

            element.Position = (CurrentRowNumber, i)
            element.ParentContainer = self
            CurrentRow.append(element)
        # -------------------------  Append the row to list of Rows  ------------------------- #
        self.Rows.append(CurrentRow)

    # ------------------------- Add Multiple Rows to Form ------------------------- #
    def AddRows(self, rows):
        """

        :param rows: 

        """
        for row in rows:
            self.AddRow(*row)

    def Layout(self, rows):
        """

        :param rows: 

        """
        self.AddRows(rows)
        self.BuildKeyDict()
        return self

    def LayoutAndRead(self, rows, non_blocking=False):
        """

        :param rows: 
        :param non_blocking:  (Default value = False)

        """
        raise DeprecationWarning(
            'LayoutAndRead is no longer supported... change your call window.Layout(layout).Read()')
        # self.AddRows(rows)
        # self.Show(non_blocking=non_blocking)
        # return self.ReturnValues

    def LayoutAndShow(self, rows):
        """

        :param rows: 

        """
        raise DeprecationWarning('LayoutAndShow is no longer supported... ')

    # ------------------------- ShowForm   THIS IS IT! ------------------------- #
    def Show(self, non_blocking=False):
        """

        :param non_blocking:  (Default value = False)

        """
        self.Shown = True
        # Compute num rows & num cols (it'll come in handy debugging)
        self.NumRows = len(self.Rows)
        self.NumCols = max(len(row) for row in self.Rows)
        self.NonBlocking = non_blocking

        # Search through entire form to see if any elements set the focus
        # if not, then will set the focus to the first input element
        found_focus = False
        for row in self.Rows:
            for element in row:
                try:
                    if element.Focus:
                        found_focus = True
                except:
                    pass
                try:
                    if element.Key is not None:
                        self.UseDictionary = True
                except:
                    pass

        if not found_focus and self.UseDefaultFocus:
            self.UseDefaultFocus = True
        else:
            self.UseDefaultFocus = False
        # -=-=-=-=-=-=-=-=- RUN the GUI -=-=-=-=-=-=-=-=- ##
        StartupTK(self)
        # If a button or keyboard event happened but no results have been built, build the results
        if self.LastKeyboardEvent is not None or self.LastButtonClicked is not None:
            return BuildResults(self, False, self)
        return self.ReturnValues

    # ------------------------- SetIcon - set the window's fav icon ------------------------- #
    def SetIcon(self, icon=None, pngbase64=None):
        """

        :param icon:  (Default value = None)
        :param pngbase64:  (Default value = None)

        """
        if type(icon) is bytes:
            wicon = tkinter.PhotoImage(data=icon)
            try:
                self.TKroot.tk.call('wm', 'iconphoto', self.TKroot._w, wicon)
            except:
                pass
        elif pngbase64 != None:
            wicon = tkinter.PhotoImage(data=pngbase64)
            try:
                self.TKroot.tk.call('wm', 'iconphoto', self.TKroot._w, wicon)
            except:
                pass
        else:
            wicon = icon

        self.WindowIcon = wicon
        try:
            self.TKroot.iconbitmap(wicon)
        except:
            pass

    def _GetElementAtLocation(self, location):
        """

        :param location: 

        """
        (row_num, col_num) = location
        row = self.Rows[row_num]
        element = row[col_num]
        return element

    def _GetDefaultElementSize(self):
        """ """
        return self.DefaultElementSize

    def _AutoCloseAlarmCallback(self):
        """ """
        try:
            window = self
            if window:
                if window.NonBlocking:
                    self.CloseNonBlockingForm()
                else:
                    window._Close()
                    self.TKroot.quit()
                    self.RootNeedsDestroying = True
        except:
            pass

    def _TimeoutAlarmCallback(self):
        """ """
        # first, get the results table built
        # modify the Results table in the parent FlexForm object
        # print('TIMEOUT CALLBACK')
        if self.TimerCancelled:
            # print('** timer was cancelled **')
            return
        self.LastButtonClicked = self.TimeoutKey
        self.FormRemainedOpen = True
        self.TKroot.quit()  # kick the users out of the mainloop

    def Read(self, timeout=None, timeout_key=TIMEOUT_KEY):
        """

        :param timeout:  (Default value = None)
        :param timeout_key:  (Default value = TIMEOUT_KEY)

        """
        # ensure called only 1 time through a single read cycle
        if not Window.read_call_from_debugger:
            refresh_debugger()
        timeout = int(timeout) if timeout is not None else None
        if timeout == 0:  # timeout of zero runs the old readnonblocking
            event, values = self.ReadNonBlocking()
            if event is None:
                event = timeout_key
            if values is None:
                event = None
            return event, values  # make event None if values was None and return
        # Read with a timeout
        self.Timeout = timeout
        self.TimeoutKey = timeout_key
        self.NonBlocking = False
        if self.TKrootDestroyed:
            return None, None
        if not self.Shown:
            self.Show()
        else:
            # if already have a button waiting, the return previously built results
            if self.LastButtonClicked is not None and not self.LastButtonClickedWasRealtime:
                # print(f'*** Found previous clicked saved {self.LastButtonClicked}')
                results = BuildResults(self, False, self)
                self.LastButtonClicked = None
                return results
            InitializeResults(self)
            # if the last button clicked was realtime, emulate a read non-blocking
            # the idea is to quickly return realtime buttons without any blocks until released
            if self.LastButtonClickedWasRealtime:
                self.LastButtonClickedWasRealtime = False  # stops from generating events until something changes

                # print(f'RTime down {self.LastButtonClicked}' )
                try:
                    rc = self.TKroot.update()
                except:
                    self.TKrootDestroyed = True
                    Window.DecrementOpenCount()
                    # _my_windows.Decrement()
                    # print('ROOT Destroyed')
                results = BuildResults(self, False, self)
                if results[0] != None and results[0] != timeout_key:
                    return results
                else:
                    pass

                # else:
                #     print("** REALTIME PROBLEM FOUND **", results)

            if self.RootNeedsDestroying:
                # print('*** DESTROYING really late***')
                self.TKroot.destroy()
                # _my_windows.Decrement()
                self.LastButtonClicked = None
                return None, None

            # normal read blocking code....
            if timeout != None:
                self.TimerCancelled = False
                self.TKAfterID = self.TKroot.after(timeout, self._TimeoutAlarmCallback)
            self.CurrentlyRunningMainloop = True
            # print(f'In main {self.Title} {self.TKroot}')
            self.TKroot.protocol("WM_DESTROY_WINDOW", self.OnClosingCallback)
            self.TKroot.protocol("WM_DELETE_WINDOW", self.OnClosingCallback)
            self.TKroot.mainloop()
            # print('Out main')
            self.CurrentlyRunningMainloop = False
            # if self.LastButtonClicked != TIMEOUT_KEY:
            #     print(f'Window {self.Title} Last button clicked = {self.LastButtonClicked}')
            try:
                self.TKroot.after_cancel(self.TKAfterID)
            except:
                pass
                # print('** tkafter cancel failed **')
            self.TimerCancelled = True
            if self.RootNeedsDestroying:
                # print('*** DESTROYING LATE ***')
                self.TKroot.destroy()
                Window.DecrementOpenCount()
                # _my_windows.Decrement()
                self.LastButtonClicked = None
                return None, None
            # if form was closed with X
            if self.LastButtonClicked is None and self.LastKeyboardEvent is None and self.ReturnValues[0] is None:
                Window.DecrementOpenCount()
                # _my_windows.Decrement()
        # Determine return values
        if self.LastKeyboardEvent is not None or self.LastButtonClicked is not None:
            results = BuildResults(self, False, self)
            if not self.LastButtonClickedWasRealtime:
                self.LastButtonClicked = None
            return results
        else:
            if not self.XFound and self.Timeout != 0 and self.Timeout is not None and self.ReturnValues[
                0] is None:  # Special Qt case because returning for no reason so fake timeout
                self.ReturnValues = self.TimeoutKey, self.ReturnValues[1]  # fake a timeout
            elif not self.XFound and self.ReturnValues[
                0] is None:  # TODO HIGHLY EXPERIMENTAL... added due to tray icon interaction
                # print("*** Faking timeout ***")
                self.ReturnValues = self.TimeoutKey, self.ReturnValues[1]  # fake a timeout
            return self.ReturnValues

    def ReadNonBlocking(self):
        """ """
        if self.TKrootDestroyed:
            try:
                self.TKroot.quit()
                self.TKroot.destroy()
            except:
                pass
                # print('DESTROY FAILED')
            return None, None
        if not self.Shown:
            self.Show(non_blocking=True)
        try:
            rc = self.TKroot.update()
        except:
            self.TKrootDestroyed = True
            Window.DecrementOpenCount()
            # _my_windows.Decrement()
            # print("read failed")
            # return None, None
        if self.RootNeedsDestroying:
            # print('*** DESTROYING LATE ***', self.ReturnValues)
            self.TKroot.destroy()
            Window.DecrementOpenCount()
            # _my_windows.Decrement()
            self.Values = None
            self.LastButtonClicked = None
            return None, None
        return BuildResults(self, False, self)

    def Finalize(self):
        """ """
        if self.TKrootDestroyed:
            return self
        if not self.Shown:
            self.Show(non_blocking=True)
        try:
            rc = self.TKroot.update()
        except:
            self.TKrootDestroyed = True
            Window.DecrementOpenCount()
            # _my_windows.Decrement()
            # return None, None
        return self

    def Refresh(self):
        """ """
        if self.TKrootDestroyed:
            return self
        try:
            rc = self.TKroot.update()
        except:
            pass
        return self

    def Fill(self, values_dict):
        """

        :param values_dict: 

        """
        FillFormWithValues(self, values_dict)
        return self

    def FindElement(self, key, silent_on_error=False):
        """

        :param key: (common_key) Used with window.FindElement and with return values
        :param silent_on_error:  (Default value = False)

        """
        # print(f'In find elem key={key}', self.AllKeysDict)

        try:
            element = self.AllKeysDict[key]
        except KeyError:
            element = None
        # element = _FindElementFromKeyInSubForm(self, key)
        if element is None:
            if not silent_on_error:
                print(
                    '*** WARNING = FindElement did not find the key. Please check your key\'s spelling key = %s ***' % key)
                PopupError('Keyword error in FindElement Call',
                           'Bad key = {}'.format(key),
                           'Your bad line of code may resemble this:',
                           'window.FindElement("{}")'.format(key))
            return ErrorElement(key=key)
        return element

    Element = FindElement  # Shortcut function
    Find = FindElement

    def FindElementWithFocus(self):
        """ """
        element = _FindElementWithFocusInSubForm(self)
        return element

    def BuildKeyDict(self):
        """ """
        dict = {}
        self.AllKeysDict = self._BuildKeyDictForWindow(self, self, dict)
        # print(f'keys built = {self.AllKeysDict}')

    def _BuildKeyDictForWindow(self, top_window, window, key_dict):
        """

        :param top_window: 
        :param window: 
        :param key_dict: 

        """
        for row_num, row in enumerate(window.Rows):
            for col_num, element in enumerate(row):
                if element.Type == ELEM_TYPE_COLUMN:
                    key_dict = self._BuildKeyDictForWindow(top_window, element, key_dict)
                if element.Type == ELEM_TYPE_FRAME:
                    key_dict = self._BuildKeyDictForWindow(top_window, element, key_dict)
                if element.Type == ELEM_TYPE_TAB_GROUP:
                    key_dict = self._BuildKeyDictForWindow(top_window, element, key_dict)
                if element.Type == ELEM_TYPE_PANE:
                    key_dict = self._BuildKeyDictForWindow(top_window, element, key_dict)
                if element.Type == ELEM_TYPE_TAB:
                    key_dict = self._BuildKeyDictForWindow(top_window, element, key_dict)
                if element.Key is None:  # if no key has been assigned.... create one for input elements
                    if element.Type == ELEM_TYPE_BUTTON:
                        element.Key = element.ButtonText
                    if element.Type in (ELEM_TYPE_MENUBAR, ELEM_TYPE_BUTTONMENU, ELEM_TYPE_CANVAS,
                                        ELEM_TYPE_INPUT_SLIDER, ELEM_TYPE_GRAPH, ELEM_TYPE_IMAGE,
                                        ELEM_TYPE_INPUT_CHECKBOX, ELEM_TYPE_INPUT_LISTBOX, ELEM_TYPE_INPUT_COMBO,
                                        ELEM_TYPE_INPUT_MULTILINE, ELEM_TYPE_INPUT_OPTION_MENU, ELEM_TYPE_INPUT_SPIN,
                                        ELEM_TYPE_INPUT_RADIO, ELEM_TYPE_INPUT_TEXT):
                        element.Key = top_window.DictionaryKeyCounter
                        top_window.DictionaryKeyCounter += 1
                if element.Key is not None:
                    if element.Key in key_dict.keys():
                        print('*** Duplicate key found in your layout {} ***'.format(
                            element.Key)) if element.Type != ELEM_TYPE_BUTTON else None
                        element.Key = element.Key + str(self.UniqueKeyCounter)
                        self.UniqueKeyCounter += 1
                        print('*** Replaced new key with {} ***'.format(
                            element.Key)) if element.Type != ELEM_TYPE_BUTTON else None
                    key_dict[element.Key] = element
        return key_dict

    def SaveToDisk(self, filename):
        """

        :param filename: 

        """
        try:
            results = BuildResults(self, False, self)
            with open(filename, 'wb') as sf:
                pickle.dump(results[1], sf)
        except:
            print('*** Error saving form to disk ***')

    def LoadFromDisk(self, filename):
        """

        :param filename: 

        """
        try:
            with open(filename, 'rb') as df:
                self.Fill(pickle.load(df))
        except:
            print('*** Error loading form to disk ***')

    def GetScreenDimensions(self):
        """ """
        if self.TKrootDestroyed:
            return None, None
        screen_width = self.TKroot.winfo_screenwidth()  # get window info to move to middle of screen
        screen_height = self.TKroot.winfo_screenheight()
        return screen_width, screen_height

    def Move(self, x, y):
        """

        :param x: 
        :param y: 

        """
        try:
            self.TKroot.geometry("+%s+%s" % (x, y))
        except:
            pass

    def Minimize(self):
        """ """
        self.TKroot.iconify()

    def Maximize(self):
        """ """
        if sys.platform != 'linux':
            self.TKroot.state('zoomed')
        else:
            self.TKroot.attributes('-fullscreen', True)
        # this method removes the titlebar too
        # self.TKroot.attributes('-fullscreen', True)

    def Normal(self):
        """ """
        if sys.platform != 'linux':
            self.TKroot.state('normal')
        else:
            self.TKroot.attributes('-fullscreen', False)

    def StartMove(self, event):
        """

        :param event: 

        """
        try:
            self.TKroot.x = event.x
            self.TKroot.y = event.y
        except:
            pass
        # print('Start move {},{}'.format(event.x,event.y))

    def StopMove(self, event):
        """

        :param event: 

        """
        try:
            self.TKroot.x = None
            self.TKroot.y = None
        except:
            pass
        # print('-Stop- move {},{}'.format(event.x,event.y))

    def OnMotion(self, event):
        """

        :param event: 

        """
        try:
            deltax = event.x - self.TKroot.x
            deltay = event.y - self.TKroot.y
            x = self.TKroot.winfo_x() + deltax
            y = self.TKroot.winfo_y() + deltay
            self.TKroot.geometry("+%s+%s" % (x, y))
            # print('{},{}'.format(x,y))
        except:
            pass

    def _KeyboardCallback(self, event):
        """

        :param event: 

        """
        self.LastButtonClicked = None
        self.FormRemainedOpen = True
        if event.char != '':
            self.LastKeyboardEvent = event.char
        else:
            self.LastKeyboardEvent = str(event.keysym) + ':' + str(event.keycode)
        if not self.NonBlocking:
            BuildResults(self, False, self)
        if self.CurrentlyRunningMainloop:  # quit if this is the current mainloop, otherwise don't quit!
            self.TKroot.quit()

    def _MouseWheelCallback(self, event):
        """

        :param event: 

        """
        self.LastButtonClicked = None
        self.FormRemainedOpen = True
        self.LastKeyboardEvent = 'MouseWheel:Down' if event.delta < 0 else 'MouseWheel:Up'
        if not self.NonBlocking:
            BuildResults(self, False, self)
        if self.CurrentlyRunningMainloop:  # quit if this is the current mainloop, otherwise don't quit!
            self.TKroot.quit()

    def _Close(self):
        """ """
        try:
            self.TKroot.update()
        except:
            pass
        if not self.NonBlocking:
            BuildResults(self, False, self)
        if self.TKrootDestroyed:
            return None
        self.TKrootDestroyed = True
        self.RootNeedsDestroying = True
        return None

    def Close(self):
        """ """
        if self.TKrootDestroyed:
            return
        try:
            self.TKroot.destroy()
            Window.DecrementOpenCount()
            # _my_windows.Decrement()
        except:
            pass
        # if down to 1 window, try and destroy the hidden window, if there is one
        if Window.NumOpenWindows == 1:
            try:
                Window.hidden_master_root.destroy()
                Window.NumOpenWindows = 0  # if no hidden window, then this won't execute
            except:
                pass

    CloseNonBlockingForm = Close
    CloseNonBlocking = Close

    # IT FINALLY WORKED! 29-Oct-2018 was the first time this damned thing got called
    def OnClosingCallback(self):
        """ """
        # global _my_windows
        # print('Got closing callback', self.DisableClose)
        if self.DisableClose:
            return
        self.XFound = True
        if self.CurrentlyRunningMainloop:  # quit if this is the current mainloop, otherwise don't quit!
            self.TKroot.quit()  # kick the users out of the mainloop
            self.TKroot.destroy()  # kick the users out of the mainloop
            self.RootNeedsDestroying = True
            self.TKrootDestroyed = True
        else:
            self.TKroot.destroy()  # kick the users out of the mainloop
            self.RootNeedsDestroying = True
        self.RootNeedsDestroying = True

        return

    def Disable(self):
        """ """
        self.TKroot.attributes('-disabled', 1)
        # self.TKroot.grab_set_global()

    def Enable(self):
        """ """
        self.TKroot.attributes('-disabled', 0)
        # self.TKroot.grab_release()

    def Hide(self):
        """ """
        self._Hidden = True
        self.TKroot.withdraw()

    def UnHide(self):
        """ """
        if self._Hidden:
            self.TKroot.deiconify()
            self._Hidden = False

    def Disappear(self):
        """ """
        self.TKroot.attributes('-alpha', 0)

    def Reappear(self):
        """ """
        self.TKroot.attributes('-alpha', 255)

    def SetAlpha(self, alpha):
        """

        :param alpha: 

        """
        # Change the window's transparency
        # :param alpha: From 0 to 1 with 0 being completely transparent
        self._AlphaChannel = alpha
        self.TKroot.attributes('-alpha', alpha)

    @property
    def AlphaChannel(self):
        """ """
        return self._AlphaChannel

    @AlphaChannel.setter
    def AlphaChannel(self, alpha):
        """

        :param alpha: 

        """
        self._AlphaChannel = alpha
        self.TKroot.attributes('-alpha', alpha)

    def BringToFront(self):
        """ """
        try:
            self.TKroot.lift()
        except:
            pass

    def CurrentLocation(self):
        """ """
        return int(self.TKroot.winfo_x()), int(self.TKroot.winfo_y())

    @property
    def Size(self):
        """ """
        win_width = self.TKroot.winfo_width()
        win_height = self.TKroot.winfo_height()
        return win_width, win_height

    @Size.setter
    def Size(self, size):
        """

        :param size: (common_key) 

        """
        try:
            self.TKroot.geometry("%sx%s" % (size[0], size[1]))
            self.TKroot.update_idletasks()
        except:
            pass

    def VisibilityChanged(self):
        """ """
        # A dummy function.  Needed in Qt but not tkinter
        return

    def SetTransparentColor(self, color):
        """

        :param color: 

        """
        try:
            self.TKroot.attributes('-transparentcolor', color)
        except:
            print('Transparent color not supported on this platform (windows only)')

    def GrabAnyWhereOn(self):
        """ """
        self.TKroot.bind("<ButtonPress-1>", self.StartMove)
        self.TKroot.bind("<ButtonRelease-1>", self.StopMove)
        self.TKroot.bind("<B1-Motion>", self.OnMotion)

    def GrabAnyWhereOff(self):
        """ """
        self.TKroot.unbind("<ButtonPress-1>")
        self.TKroot.unbind("<ButtonRelease-1>")
        self.TKroot.unbind("<B1-Motion>")

    def _callback_main_debugger_window_create_keystroke(self, event):
        """

        :param event: 

        """
        Debugger.debugger._build_main_debugger_window()

    def _callback_popout_window_create_keystroke(self, event):
        """

        :param event: 

        """
        Debugger.debugger._build_floating_window()

    def EnableDebugger(self):
        """ """
        self.TKroot.bind('<Cancel>', self._callback_main_debugger_window_create_keystroke)
        self.TKroot.bind('<Pause>', self._callback_popout_window_create_keystroke)
        self.DebuggerEnabled = True


    def DisableDebugger(self):
        """ """
        self.TKroot.unbind("<Cancel>")
        self.TKroot.unbind("<Pause>")
        self.DebuggerEnabled = False

    def __enter__(self):
        """ """
        return self

    def __exit__(self, *a):
        """

        :param *a: 

        """
        self.__del__()
        return False

    def __del__(self):
        """ """
        # print('DELETING WINDOW')
        for row in self.Rows:
            for element in row:
                element.__del__()


FlexForm = Window


# ################################################################################
# ################################################################################
#  END OF ELEMENT DEFINITIONS
# ################################################################################
# ################################################################################


# =========================================================================== #
# Button Lazy Functions so the caller doesn't have to define a bunch of stuff #
# =========================================================================== #


# -------------------------  FOLDER BROWSE Element lazy function  ------------------------- #
def FolderBrowse(button_text='Browse', target=(ThisRow, -1), initial_folder=None, tooltip=None, size=(None, None),
                 auto_size_button=None, button_color=None, disabled=False, change_submits=False, enable_events=False,
                 font=None, pad=None, key=None):
    """

    :param button_text:  (Default value = 'Browse')
    :param target:  (Default value = (ThisRow, -1))
    :param initial_folder:  (Default value = None)
    :param tooltip: text, that will appear the you hover on (Default value = None)
    :param size: (common_key) (w,h) w=characters-wide, h=rows-high (Default value = (None, None))
    :param auto_size_button:  (Default value = None)
    :param button_color:  (Default value = None)
    :param disabled: set disable state for element (Default value = False)
    :param change_submits: If True, pressing Enter key submits window (Default value = False)
    :param enable_events: Turns on the element specific events.(Default value = False)
    :param font: (common_key) specifies the font family, size, etc (Default value = None)
    :param pad: (common_key) Amount of padding to put around element (Default value = None)
    :param key: (common_key) Used with window.FindElement and with return values (Default value = None)

    """
    
    return Button(button_text=button_text, button_type=BUTTON_TYPE_BROWSE_FOLDER, target=target,
                  initial_folder=initial_folder, tooltip=tooltip, size=size, auto_size_button=auto_size_button,
                  disabled=disabled, button_color=button_color, change_submits=change_submits,
                  enable_events=enable_events, font=font, pad=pad, key=key)


# -------------------------  FILE BROWSE Element lazy function  ------------------------- #
def FileBrowse(button_text='Browse', target=(ThisRow, -1), file_types=(("ALL Files", "*.*"),), initial_folder=None,
               tooltip=None, size=(None, None), auto_size_button=None, button_color=None, change_submits=False,
               enable_events=False, font=None, disabled=False,
               pad=None, key=None):
    """

    :param button_text:  (Default value = 'Browse')
    :param target:  (Default value = (ThisRow, -1))
    :param file_types:  (Default value = (("ALL Files", "*.*")))
    :param initial_folder:  (Default value = None)
    :param tooltip: text, that will appear the you hover on (Default value = None)
    :param size: (common_key) (w,h) w=characters-wide, h=rows-high (Default value = (None, None))
    :param auto_size_button:  (Default value = None)
    :param button_color:  (Default value = None)
    :param change_submits: If True, pressing Enter key submits window (Default value = False)
    :param enable_events: Turns on the element specific events.(Default value = False)
    :param font: (common_key) specifies the font family, size, etc (Default value = None)
    :param disabled: set disable state for element (Default value = False)
    :param pad: (common_key) Amount of padding to put around element (Default value = None)
    :param key: (common_key) Used with window.FindElement and with return values (Default value = None)

    """
    return Button(button_text=button_text, button_type=BUTTON_TYPE_BROWSE_FILE, target=target, file_types=file_types,
                  initial_folder=initial_folder, tooltip=tooltip, size=size, auto_size_button=auto_size_button,
                  change_submits=change_submits, enable_events=enable_events, disabled=disabled,
                  button_color=button_color, font=font, pad=pad, key=key)


# -------------------------  FILES BROWSE Element (Multiple file selection) lazy function  ------------------------- #
def FilesBrowse(button_text='Browse', target=(ThisRow, -1), file_types=(("ALL Files", "*.*"),), disabled=False,
                initial_folder=None, tooltip=None, size=(None, None), auto_size_button=None, button_color=None,
                change_submits=False, enable_events=False,
                font=None, pad=None, key=None):
    """

    :param button_text:  (Default value = 'Browse')
    :param target:  (Default value = (ThisRow, -1))
    :param file_types:  (Default value = (("ALL Files", "*.*")))
    :param disabled: set disable state for element (Default value = False)
    :param initial_folder:  (Default value = None)
    :param tooltip: text, that will appear the you hover on (Default value = None)
    :param size: (common_key) (w,h) w=characters-wide, h=rows-high (Default value = (None, None))
    :param auto_size_button:  (Default value = None)
    :param button_color:  (Default value = None)
    :param change_submits: If True, pressing Enter key submits window (Default value = False)
    :param enable_events: Turns on the element specific events.(Default value = False)
    :param font: (common_key) specifies the font family, size, etc (Default value = None)
    :param pad: (common_key) Amount of padding to put around element (Default value = None)
    :param key: (common_key) Used with window.FindElement and with return values (Default value = None)

    """
    return Button(button_text=button_text, button_type=BUTTON_TYPE_BROWSE_FILES, target=target, file_types=file_types,
                  initial_folder=initial_folder, change_submits=change_submits, enable_events=enable_events,
                  tooltip=tooltip, size=size, auto_size_button=auto_size_button,
                  disabled=disabled, button_color=button_color, font=font, pad=pad, key=key)


# -------------------------  FILE BROWSE Element lazy function  ------------------------- #
def FileSaveAs(button_text='Save As...', target=(ThisRow, -1), file_types=(("ALL Files", "*.*"),), initial_folder=None,
               disabled=False, tooltip=None, size=(None, None), auto_size_button=None, button_color=None,
               change_submits=False, enable_events=False, font=None,
               pad=None, key=None):
    """

    :param button_text:  (Default value = 'Save As...')
    :param target:  (Default value = (ThisRow, -1))
    :param file_types:  (Default value = (("ALL Files", "*.*")))
    :param initial_folder:  (Default value = None)
    :param disabled: set disable state for element (Default value = False)
    :param tooltip: text, that will appear the you hover on (Default value = None)
    :param size: (common_key) (w,h) w=characters-wide, h=rows-high (Default value = (None, None))
    :param auto_size_button:  (Default value = None)
    :param button_color:  (Default value = None)
    :param change_submits: If True, pressing Enter key submits window (Default value = False)
    :param enable_events: Turns on the element specific events.(Default value = False)
    :param font: (common_key) specifies the font family, size, etc (Default value = None)
    :param pad: (common_key) Amount of padding to put around element (Default value = None)
    :param key: (common_key) Used with window.FindElement and with return values (Default value = None)

    """
    return Button(button_text=button_text, button_type=BUTTON_TYPE_SAVEAS_FILE, target=target, file_types=file_types,
                  initial_folder=initial_folder, tooltip=tooltip, size=size, disabled=disabled,
                  auto_size_button=auto_size_button, button_color=button_color, change_submits=change_submits,
                  enable_events=enable_events, font=font, pad=pad, key=key)


# -------------------------  SAVE AS Element lazy function  ------------------------- #
def SaveAs(button_text='Save As...', target=(ThisRow, -1), file_types=(("ALL Files", "*.*"),), initial_folder=None,
           disabled=False, tooltip=None, size=(None, None), auto_size_button=None, button_color=None,
           change_submits=False, enable_events=False, font=None,
           pad=None, key=None):
    """

    :param button_text:  (Default value = 'Save As...')
    :param target:  (Default value = (ThisRow, -1))
    :param file_types:  (Default value = (("ALL Files", "*.*")))
    :param initial_folder:  (Default value = None)
    :param disabled: set disable state for element (Default value = False)
    :param tooltip: text, that will appear the you hover on (Default value = None)
    :param size: (common_key) (w,h) w=characters-wide, h=rows-high (Default value = (None, None))
    :param auto_size_button:  (Default value = None)
    :param button_color:  (Default value = None)
    :param change_submits: If True, pressing Enter key submits window (Default value = False)
    :param enable_events: Turns on the element specific events.(Default value = False)
    :param font: (common_key) specifies the font family, size, etc (Default value = None)
    :param pad: (common_key) Amount of padding to put around element (Default value = None)
    :param key: (common_key) Used with window.FindElement and with return values (Default value = None)

    """
    return Button(button_text=button_text, button_type=BUTTON_TYPE_SAVEAS_FILE, target=target, file_types=file_types,
                  initial_folder=initial_folder, tooltip=tooltip, size=size, disabled=disabled,
                  auto_size_button=auto_size_button, button_color=button_color, change_submits=change_submits,
                  enable_events=enable_events, font=font, pad=pad, key=key)


# -------------------------  SAVE BUTTON Element lazy function  ------------------------- #
def Save(button_text='Save', size=(None, None), auto_size_button=None, button_color=None, bind_return_key=True,
         disabled=False, tooltip=None, font=None, focus=False, pad=None, key=None):
    """

    :param button_text:  (Default value = 'Save')
    :param size: (common_key) (w,h) w=characters-wide, h=rows-high (Default value = (None, None))
    :param auto_size_button:  (Default value = None)
    :param button_color:  (Default value = None)
    :param bind_return_key:  (Default value = True)
    :param disabled: set disable state for element (Default value = False)
    :param tooltip: text, that will appear the you hover on (Default value = None)
    :param font: (common_key) specifies the font family, size, etc (Default value = None)
    :param focus: if focus should be set to this (Default value = None)
    :param pad: (common_key) Amount of padding to put around element (Default value = None)
    :param key: (common_key) Used with window.FindElement and with return values (Default value = None)

    """
    return Button(button_text=button_text, button_type=BUTTON_TYPE_READ_FORM, tooltip=tooltip, size=size,
                  auto_size_button=auto_size_button, button_color=button_color, font=font, disabled=disabled,
                  bind_return_key=bind_return_key, focus=focus, pad=pad, key=key)


# -------------------------  SUBMIT BUTTON Element lazy function  ------------------------- #
def Submit(button_text='Submit', size=(None, None), auto_size_button=None, button_color=None, disabled=False,
           bind_return_key=True, tooltip=None, font=None, focus=False, pad=None, key=None):
    """

    :param button_text:  (Default value = 'Submit')
    :param size: (common_key) (w,h) w=characters-wide, h=rows-high (Default value = (None, None))
    :param auto_size_button:  (Default value = None)
    :param button_color:  (Default value = None)
    :param disabled: set disable state for element (Default value = False)
    :param bind_return_key:  (Default value = True)
    :param tooltip: text, that will appear the you hover on (Default value = None)
    :param font: (common_key) specifies the font family, size, etc (Default value = None)
    :param focus: if focus should be set to this (Default value = None)
    :param pad: (common_key) Amount of padding to put around element (Default value = None)
    :param key: (common_key) Used with window.FindElement and with return values (Default value = None)

    """
    return Button(button_text=button_text, button_type=BUTTON_TYPE_READ_FORM, tooltip=tooltip, size=size,
                  auto_size_button=auto_size_button, button_color=button_color, font=font, disabled=disabled,
                  bind_return_key=bind_return_key, focus=focus, pad=pad, key=key)


# -------------------------  OPEN BUTTON Element lazy function  ------------------------- #
# -------------------------  OPEN BUTTON Element lazy function  ------------------------- #
def Open(button_text='Open', size=(None, None), auto_size_button=None, button_color=None, disabled=False,
         bind_return_key=True, tooltip=None, font=None, focus=False, pad=None, key=None):
    """

    :param button_text:  (Default value = 'Open')
    :param size: (common_key) (w,h) w=characters-wide, h=rows-high (Default value = (None, None))
    :param auto_size_button:  (Default value = None)
    :param button_color:  (Default value = None)
    :param disabled: set disable state for element (Default value = False)
    :param bind_return_key:  (Default value = True)
    :param tooltip: text, that will appear the you hover on (Default value = None)
    :param font: (common_key) specifies the font family, size, etc (Default value = None)
    :param focus: if focus should be set to this (Default value = None)
    :param pad: (common_key) Amount of padding to put around element (Default value = None)
    :param key: (common_key) Used with window.FindElement and with return values (Default value = None)

    """
    return Button(button_text=button_text, button_type=BUTTON_TYPE_READ_FORM, tooltip=tooltip, size=size,
                  auto_size_button=auto_size_button, button_color=button_color, font=font, disabled=disabled,
                  bind_return_key=bind_return_key, focus=focus, pad=pad, key=key)


# -------------------------  OK BUTTON Element lazy function  ------------------------- #
def OK(button_text='OK', size=(None, None), auto_size_button=None, button_color=None, disabled=False,
       bind_return_key=True, tooltip=None, font=None, focus=False, pad=None, key=None):
    """

    :param button_text:  (Default value = 'OK')
    :param size: (common_key) (w,h) w=characters-wide, h=rows-high (Default value = (None, None))
    :param auto_size_button:  (Default value = None)
    :param button_color:  (Default value = None)
    :param disabled: set disable state for element (Default value = False)
    :param bind_return_key:  (Default value = True)
    :param tooltip: text, that will appear the you hover on (Default value = None)
    :param font: (common_key) specifies the font family, size, etc (Default value = None)
    :param focus: if focus should be set to this (Default value = None)
    :param pad: (common_key) Amount of padding to put around element (Default value = None)
    :param key: (common_key) Used with window.FindElement and with return values (Default value = None)

    """
    return Button(button_text=button_text, button_type=BUTTON_TYPE_READ_FORM, tooltip=tooltip, size=size,
                  auto_size_button=auto_size_button, button_color=button_color, font=font, disabled=disabled,
                  bind_return_key=bind_return_key, focus=focus, pad=pad, key=key)


# -------------------------  YES BUTTON Element lazy function  ------------------------- #
def Ok(button_text='Ok', size=(None, None), auto_size_button=None, button_color=None, disabled=False,
       bind_return_key=True, tooltip=None, font=None, focus=False, pad=None, key=None):
    """

    :param button_text:  (Default value = 'Ok')
    :param size: (common_key) (w,h) w=characters-wide, h=rows-high (Default value = (None, None))
    :param auto_size_button:  (Default value = None)
    :param button_color:  (Default value = None)
    :param disabled: set disable state for element (Default value = False)
    :param bind_return_key:  (Default value = True)
    :param tooltip: text, that will appear the you hover on (Default value = None)
    :param font: (common_key) specifies the font family, size, etc (Default value = None)
    :param focus: if focus should be set to this (Default value = None)
    :param pad: (common_key) Amount of padding to put around element (Default value = None)
    :param key: (common_key) Used with window.FindElement and with return values (Default value = None)

    """
    return Button(button_text=button_text, button_type=BUTTON_TYPE_READ_FORM, tooltip=tooltip, size=size,
                  auto_size_button=auto_size_button, button_color=button_color, font=font, disabled=disabled,
                  bind_return_key=bind_return_key, focus=focus, pad=pad, key=key)


# -------------------------  CANCEL BUTTON Element lazy function  ------------------------- #
def Cancel(button_text='Cancel', size=(None, None), auto_size_button=None, button_color=None, disabled=False,
           tooltip=None, font=None, bind_return_key=False, focus=False, pad=None, key=None):
    """

    :param button_text:  (Default value = 'Cancel')
    :param size: (common_key) (w,h) w=characters-wide, h=rows-high (Default value = (None, None))
    :param auto_size_button:  (Default value = None)
    :param button_color:  (Default value = None)
    :param disabled: set disable state for element (Default value = False)
    :param tooltip: text, that will appear the you hover on (Default value = None)
    :param font: (common_key) specifies the font family, size, etc (Default value = None)
    :param bind_return_key:  (Default value = False)
    :param focus: if focus should be set to this (Default value = None)
    :param pad: (common_key) Amount of padding to put around element (Default value = None)
    :param key: (common_key) Used with window.FindElement and with return values (Default value = None)

    """
    return Button(button_text=button_text, button_type=BUTTON_TYPE_READ_FORM, tooltip=tooltip, size=size,
                  auto_size_button=auto_size_button, button_color=button_color, font=font, disabled=disabled,
                  bind_return_key=bind_return_key, focus=focus, pad=pad, key=key)


# -------------------------  QUIT BUTTON Element lazy function  ------------------------- #
def Quit(button_text='Quit', size=(None, None), auto_size_button=None, button_color=None, disabled=False, tooltip=None,
         font=None, bind_return_key=False, focus=False, pad=None, key=None):
    """

    :param button_text:  (Default value = 'Quit')
    :param size: (common_key) (w,h) w=characters-wide, h=rows-high (Default value = (None, None))
    :param auto_size_button:  (Default value = None)
    :param button_color:  (Default value = None)
    :param disabled: set disable state for element (Default value = False)
    :param tooltip: text, that will appear the you hover on (Default value = None)
    :param font: (common_key) specifies the font family, size, etc (Default value = None)
    :param bind_return_key:  (Default value = False)
    :param focus: if focus should be set to this (Default value = None)
    :param pad: (common_key) Amount of padding to put around element (Default value = None)
    :param key: (common_key) Used with window.FindElement and with return values (Default value = None)

    """
    return Button(button_text=button_text, button_type=BUTTON_TYPE_READ_FORM, tooltip=tooltip, size=size,
                  auto_size_button=auto_size_button, button_color=button_color, font=font, disabled=disabled,
                  bind_return_key=bind_return_key, focus=focus, pad=pad, key=key)


# -------------------------  Exit BUTTON Element lazy function  ------------------------- #
def Exit(button_text='Exit', size=(None, None), auto_size_button=None, button_color=None, disabled=False, tooltip=None,
         font=None, bind_return_key=False, focus=False, pad=None, key=None):
    """

    :param button_text:  (Default value = 'Exit')
    :param size: (common_key) (w,h) w=characters-wide, h=rows-high (Default value = (None, None))
    :param auto_size_button:  (Default value = None)
    :param button_color:  (Default value = None)
    :param disabled: set disable state for element (Default value = False)
    :param tooltip: text, that will appear the you hover on (Default value = None)
    :param font: (common_key) specifies the font family, size, etc (Default value = None)
    :param bind_return_key:  (Default value = False)
    :param focus: if focus should be set to this (Default value = None)
    :param pad: (common_key) Amount of padding to put around element (Default value = None)
    :param key: (common_key) Used with window.FindElement and with return values (Default value = None)

    """
    return Button(button_text=button_text, button_type=BUTTON_TYPE_READ_FORM, tooltip=tooltip, size=size,
                  auto_size_button=auto_size_button, button_color=button_color, font=font, disabled=disabled,
                  bind_return_key=bind_return_key, focus=focus, pad=pad, key=key)


# -------------------------  YES BUTTON Element lazy function  ------------------------- #
def Yes(button_text='Yes', size=(None, None), auto_size_button=None, button_color=None, disabled=False, tooltip=None,
        font=None, bind_return_key=True, focus=False, pad=None, key=None):
    """

    :param button_text:  (Default value = 'Yes')
    :param size: (common_key) (w,h) w=characters-wide, h=rows-high (Default value = (None, None))
    :param auto_size_button:  (Default value = None)
    :param button_color:  (Default value = None)
    :param disabled: set disable state for element (Default value = False)
    :param tooltip: text, that will appear the you hover on (Default value = None)
    :param font: (common_key) specifies the font family, size, etc (Default value = None)
    :param bind_return_key:  (Default value = True)
    :param focus: if focus should be set to this (Default value = None)
    :param pad: (common_key) Amount of padding to put around element (Default value = None)
    :param key: (common_key) Used with window.FindElement and with return values (Default value = None)

    """
    return Button(button_text=button_text, button_type=BUTTON_TYPE_READ_FORM, tooltip=tooltip, size=size,
                  auto_size_button=auto_size_button, button_color=button_color, font=font, disabled=disabled,
                  bind_return_key=bind_return_key, focus=focus, pad=pad, key=key)


# -------------------------  NO BUTTON Element lazy function  ------------------------- #
def No(button_text='No', size=(None, None), auto_size_button=None, button_color=None, disabled=False, tooltip=None,
       font=None, bind_return_key=False, focus=False, pad=None, key=None):
    """

    :param button_text:  (Default value = 'No')
    :param size: (common_key) (w,h) w=characters-wide, h=rows-high (Default value = (None, None))
    :param auto_size_button:  (Default value = None)
    :param button_color:  (Default value = None)
    :param disabled: set disable state for element (Default value = False)
    :param tooltip: text, that will appear the you hover on (Default value = None)
    :param font: (common_key) specifies the font family, size, etc (Default value = None)
    :param bind_return_key:  (Default value = False)
    :param focus: if focus should be set to this (Default value = None)
    :param pad: (common_key) Amount of padding to put around element (Default value = None)
    :param key: (common_key) Used with window.FindElement and with return values (Default value = None)

    """
    return Button(button_text=button_text, button_type=BUTTON_TYPE_READ_FORM, tooltip=tooltip, size=size,
                  auto_size_button=auto_size_button, button_color=button_color, font=font, disabled=disabled,
                  bind_return_key=bind_return_key, focus=focus, pad=pad, key=key)


# -------------------------  NO BUTTON Element lazy function  ------------------------- #
def Help(button_text='Help', size=(None, None), auto_size_button=None, button_color=None, disabled=False, font=None,
         tooltip=None, bind_return_key=False, focus=False, pad=None, key=None):
    """

    :param button_text:  (Default value = 'Help')
    :param size: (common_key) (w,h) w=characters-wide, h=rows-high (Default value = (None, None))
    :param auto_size_button:  (Default value = None)
    :param button_color:  (Default value = None)
    :param disabled: set disable state for element (Default value = False)
    :param font: (common_key) specifies the font family, size, etc (Default value = None)
    :param tooltip: text, that will appear the you hover on (Default value = None)
    :param bind_return_key:  (Default value = False)
    :param focus: if focus should be set to this (Default value = None)
    :param pad: (common_key) Amount of padding to put around element (Default value = None)
    :param key: (common_key) Used with window.FindElement and with return values (Default value = None)

    """
    return Button(button_text=button_text, button_type=BUTTON_TYPE_READ_FORM, tooltip=tooltip, size=size,
                  auto_size_button=auto_size_button, button_color=button_color, font=font, disabled=disabled,
                  bind_return_key=bind_return_key, focus=focus, pad=pad, key=key)


# -------------------------  NO BUTTON Element lazy function  ------------------------- #
def Debug(button_text='', size=(None, None), auto_size_button=None, button_color=None, disabled=False, font=None,
          tooltip=None, bind_return_key=False, focus=False, pad=None, key=None):
    """

    :param button_text:  (Default value = '')
    :param size: (common_key) (w,h) w=characters-wide, h=rows-high (Default value = (None, None))
    :param auto_size_button:  (Default value = None)
    :param button_color:  (Default value = None)
    :param disabled: set disable state for element (Default value = False)
    :param font: (common_key) specifies the font family, size, etc (Default value = None)
    :param tooltip: text, that will appear the you hover on (Default value = None)
    :param bind_return_key:  (Default value = False)
    :param focus: if focus should be set to this (Default value = None)
    :param pad: (common_key) Amount of padding to put around element (Default value = None)
    :param key: (common_key) Used with window.FindElement and with return values (Default value = None)

    """
    return Button(button_text=button_text, button_type=BUTTON_TYPE_SHOW_DEBUGGER, tooltip=tooltip, size=size,
                  auto_size_button=auto_size_button, button_color=COLOR_SYSTEM_DEFAULT, font=font, disabled=disabled,
                  bind_return_key=bind_return_key, focus=focus, pad=pad, key=key, image_data=PSG_DEBUGGER_LOGO,
                  image_subsample=4, border_width=0)


# -------------------------  GENERIC BUTTON Element lazy function  ------------------------- #
def SimpleButton(button_text, image_filename=None, image_data=None, image_size=(None, None), image_subsample=None,
                 border_width=None, tooltip=None, size=(None, None), auto_size_button=None, button_color=None,
                 font=None, bind_return_key=False, disabled=False, focus=False, pad=None, key=None):
    """

    :param button_text: 
    :param image_filename:  (Default value = None)
    :param image_data:  (Default value = None)
    :param image_size:  (Default value = (None, None))
    :param image_subsample:  (Default value = None)
    :param border_width:  (Default value = None)
    :param tooltip: text, that will appear the you hover on (Default value = None)
    :param size: (common_key) (w,h) w=characters-wide, h=rows-high (Default value = (None)
    :param auto_size_button:  (Default value = None)
    :param button_color:  (Default value = None)
    :param font: (common_key) specifies the font family, size, etc (Default value = None)
    :param bind_return_key:  (Default value = False)
    :param disabled: set disable state for element (Default value = False)
    :param focus: if focus should be set to this (Default value = None)
    :param pad: (common_key) Amount of padding to put around element (Default value = None)
    :param key: (common_key) Used with window.FindElement and with return values (Default value = None)

    """
    return Button(button_text=button_text, button_type=BUTTON_TYPE_CLOSES_WIN, image_filename=image_filename,
                  image_data=image_data, image_size=image_size, image_subsample=image_subsample,
                  border_width=border_width, tooltip=tooltip, disabled=disabled, size=size,
                  auto_size_button=auto_size_button, button_color=button_color, font=font,
                  bind_return_key=bind_return_key, focus=focus, pad=pad, key=key)


# -------------------------  CLOSE BUTTON Element lazy function  ------------------------- #
def CloseButton(button_text, image_filename=None, image_data=None, image_size=(None, None), image_subsample=None,
                border_width=None, tooltip=None, size=(None, None), auto_size_button=None, button_color=None, font=None,
                bind_return_key=False, disabled=False, focus=False, pad=None, key=None):
    """

    :param button_text: 
    :param image_filename:  (Default value = None)
    :param image_data:  (Default value = None)
    :param image_size:  (Default value = (None, None))
    :param image_subsample:  (Default value = None)
    :param border_width:  (Default value = None)
    :param tooltip: text, that will appear the you hover on (Default value = None)
    :param size: (common_key) (w,h) w=characters-wide, h=rows-high (Default value = (None)
    :param auto_size_button:  (Default value = None)
    :param button_color:  (Default value = None)
    :param font: (common_key) specifies the font family, size, etc (Default value = None)
    :param bind_return_key:  (Default value = False)
    :param disabled: set disable state for element (Default value = False)
    :param focus: if focus should be set to this (Default value = None)
    :param pad: (common_key) Amount of padding to put around element (Default value = None)
    :param key: (common_key) Used with window.FindElement and with return values (Default value = None)

    """
    return Button(button_text=button_text, button_type=BUTTON_TYPE_CLOSES_WIN, image_filename=image_filename,
                  image_data=image_data, image_size=image_size, image_subsample=image_subsample,
                  border_width=border_width, tooltip=tooltip, disabled=disabled, size=size,
                  auto_size_button=auto_size_button, button_color=button_color, font=font,
                  bind_return_key=bind_return_key, focus=focus, pad=pad, key=key)


CButton = CloseButton


# -------------------------  GENERIC BUTTON Element lazy function  ------------------------- #
def ReadButton(button_text, image_filename=None, image_data=None, image_size=(None, None), image_subsample=None,
               border_width=None, tooltip=None, size=(None, None), auto_size_button=None, button_color=None, font=None,
               bind_return_key=False, disabled=False, focus=False, pad=None, key=None):
    """

    :param button_text: 
    :param image_filename:  (Default value = None)
    :param image_data:  (Default value = None)
    :param image_size:  (Default value = (None, None))
    :param image_subsample:  (Default value = None)
    :param border_width:  (Default value = None)
    :param tooltip: text, that will appear the you hover on (Default value = None)
    :param size: (common_key) (w,h) w=characters-wide, h=rows-high (Default value = (None)
    :param auto_size_button:  (Default value = None)
    :param button_color:  (Default value = None)
    :param font: (common_key) specifies the font family, size, etc (Default value = None)
    :param bind_return_key:  (Default value = False)
    :param disabled: set disable state for element (Default value = False)
    :param focus: if focus should be set to this (Default value = None)
    :param pad: (common_key) Amount of padding to put around element (Default value = None)
    :param key: (common_key) Used with window.FindElement and with return values (Default value = None)

    """
    return Button(button_text=button_text, button_type=BUTTON_TYPE_READ_FORM, image_filename=image_filename,
                  image_data=image_data, image_size=image_size, image_subsample=image_subsample,
                  border_width=border_width, tooltip=tooltip, size=size, disabled=disabled,
                  auto_size_button=auto_size_button, button_color=button_color, font=font,
                  bind_return_key=bind_return_key, focus=focus, pad=pad, key=key)


ReadFormButton = ReadButton
RButton = ReadFormButton


# -------------------------  Realtime BUTTON Element lazy function  ------------------------- #
def RealtimeButton(button_text, image_filename=None, image_data=None, image_size=(None, None), image_subsample=None,
                   border_width=None, tooltip=None, size=(None, None), auto_size_button=None, button_color=None,
                   font=None, disabled=False, bind_return_key=False, focus=False, pad=None, key=None):
    """

    :param button_text: 
    :param image_filename:  (Default value = None)
    :param image_data:  (Default value = None)
    :param image_size:  (Default value = (None, None))
    :param image_subsample:  (Default value = None)
    :param border_width:  (Default value = None)
    :param tooltip: text, that will appear the you hover on (Default value = None)
    :param size: (common_key) (w,h) w=characters-wide, h=rows-high (Default value = (None)
    :param auto_size_button:  (Default value = None)
    :param button_color:  (Default value = None)
    :param font: (common_key) specifies the font family, size, etc (Default value = None)
    :param disabled: set disable state for element (Default value = False)
    :param bind_return_key:  (Default value = False)
    :param focus: if focus should be set to this (Default value = None)
    :param pad: (common_key) Amount of padding to put around element (Default value = None)
    :param key: (common_key) Used with window.FindElement and with return values (Default value = None)

    """
    return Button(button_text=button_text, button_type=BUTTON_TYPE_REALTIME, image_filename=image_filename,
                  image_data=image_data, image_size=image_size, image_subsample=image_subsample,
                  border_width=border_width, tooltip=tooltip, disabled=disabled, size=size,
                  auto_size_button=auto_size_button, button_color=button_color, font=font,
                  bind_return_key=bind_return_key, focus=focus, pad=pad, key=key)


# -------------------------  Dummy BUTTON Element lazy function  ------------------------- #
def DummyButton(button_text, image_filename=None, image_data=None, image_size=(None, None), image_subsample=None,
                border_width=None, tooltip=None, size=(None, None), auto_size_button=None, button_color=None, font=None,
                disabled=False, bind_return_key=False, focus=False, pad=None, key=None):
    """

    :param button_text: 
    :param image_filename:  (Default value = None)
    :param image_data:  (Default value = None)
    :param image_size:  (Default value = (None, None))
    :param image_subsample:  (Default value = None)
    :param border_width:  (Default value = None)
    :param tooltip: text, that will appear the you hover on (Default value = None)
    :param size: (common_key) (w,h) w=characters-wide, h=rows-high (Default value = (None)
    :param auto_size_button:  (Default value = None)
    :param button_color:  (Default value = None)
    :param font: (common_key) specifies the font family, size, etc (Default value = None)
    :param disabled: set disable state for element (Default value = False)
    :param bind_return_key:  (Default value = False)
    :param focus: if focus should be set to this (Default value = None)
    :param pad: (common_key) Amount of padding to put around element (Default value = None)
    :param key: (common_key) Used with window.FindElement and with return values (Default value = None)

    """
    return Button(button_text=button_text, button_type=BUTTON_TYPE_CLOSES_WIN_ONLY, image_filename=image_filename,
                  image_data=image_data, image_size=image_size, image_subsample=image_subsample,
                  border_width=border_width, tooltip=tooltip, size=size, auto_size_button=auto_size_button,
                  button_color=button_color, font=font, disabled=disabled, bind_return_key=bind_return_key, focus=focus,
                  pad=pad, key=key)


# -------------------------  Calendar Chooser Button lazy function  ------------------------- #
def CalendarButton(button_text, target=(None, None), close_when_date_chosen=True, default_date_m_d_y=(None, None, None),
                   image_filename=None, image_data=None, image_size=(None, None),
                   image_subsample=None, tooltip=None, border_width=None, size=(None, None), auto_size_button=None,
                   button_color=None, disabled=False, font=None, bind_return_key=False, focus=False, pad=None,
                   key=None, locale=None, format=None):
    """

    :param button_text: 
    :param target:  (Default value = (None, None))
    :param close_when_date_chosen:  (Default value = True)
    :param default_date_m_d_y:  (Default value = (None)
    :param None: 
    :param image_filename:  (Default value = None)
    :param image_data:  (Default value = None)
    :param image_size:  (Default value = (None)
    :param image_subsample:  (Default value = None)
    :param tooltip: text, that will appear the you hover on (Default value = None)
    :param border_width:  (Default value = None)
    :param size: (common_key) (w,h) w=characters-wide, h=rows-high (Default value = (None)
    :param auto_size_button:  (Default value = None)
    :param button_color:  (Default value = None)
    :param disabled: set disable state for element (Default value = False)
    :param font: (common_key) specifies the font family, size, etc (Default value = None)
    :param bind_return_key:  (Default value = False)
    :param focus: if focus should be set to this (Default value = None)
    :param pad: (common_key) Amount of padding to put around element (Default value = None)
    :param key: (common_key) Used with window.FindElement and with return values (Default value = None)
    :param locale:  (Default value = None)
    :param format:  (Default value = None)

    """
    button = Button(button_text=button_text, button_type=BUTTON_TYPE_CALENDAR_CHOOSER, target=target,
                    image_filename=image_filename, image_data=image_data, image_size=image_size,
                    image_subsample=image_subsample, border_width=border_width, tooltip=tooltip, size=size,
                    auto_size_button=auto_size_button, button_color=button_color, font=font, disabled=disabled,
                    bind_return_key=bind_return_key, focus=focus, pad=pad, key=key)
    button.CalendarCloseWhenChosen = close_when_date_chosen
    button.DefaultDate_M_D_Y = default_date_m_d_y
    button.CalendarLocale = locale
    button.CalendarFormat = format
    return button


# -------------------------  Calendar Chooser Button lazy function  ------------------------- #
def ColorChooserButton(button_text, target=(None, None), image_filename=None, image_data=None, image_size=(None, None),
                       image_subsample=None, tooltip=None, border_width=None, size=(None, None), auto_size_button=None,
                       button_color=None, disabled=False, font=None, bind_return_key=False, focus=False, pad=None,
                       key=None):
    """

    :param button_text: 
    :param target:  (Default value = (None, None))
    :param image_filename:  (Default value = None)
    :param image_data:  (Default value = None)
    :param image_size:  (Default value = (None)
    :param image_subsample:  (Default value = None)
    :param tooltip: text, that will appear the you hover on (Default value = None)
    :param border_width:  (Default value = None)
    :param size: (common_key) (w,h) w=characters-wide, h=rows-high (Default value = (None)
    :param auto_size_button:  (Default value = None)
    :param button_color:  (Default value = None)
    :param disabled: set disable state for element (Default value = False)
    :param font: (common_key) specifies the font family, size, etc (Default value = None)
    :param bind_return_key:  (Default value = False)
    :param focus: if focus should be set to this (Default value = None)
    :param pad: (common_key) Amount of padding to put around element (Default value = None)
    :param key: (common_key) Used with window.FindElement and with return values (Default value = None)

    """
    return Button(button_text=button_text, button_type=BUTTON_TYPE_COLOR_CHOOSER, target=target,
                  image_filename=image_filename, image_data=image_data, image_size=image_size,
                  image_subsample=image_subsample, border_width=border_width, tooltip=tooltip, size=size,
                  auto_size_button=auto_size_button, button_color=button_color, font=font, disabled=disabled,
                  bind_return_key=bind_return_key, focus=focus, pad=pad, key=key)


#####################################  -----  RESULTS   ------ ##################################################

def AddToReturnDictionary(form, element, value):
    """

    :param form: 
    :param element: 
    :param value: 

    """
    form.ReturnValuesDictionary[element.Key] = value
    return
    # if element.Key is None:
    #     form.ReturnValuesDictionary[form.DictionaryKeyCounter] = value
    #     element.Key = form.DictionaryKeyCounter
    #     form.DictionaryKeyCounter += 1
    # else:
    #     form.ReturnValuesDictionary[element.Key] = value


def AddToReturnList(form, value):
    """

    :param form: 
    :param value: 

    """
    form.ReturnValuesList.append(value)


# ----------------------------------------------------------------------------#
# -------  FUNCTION InitializeResults.  Sets up form results matrix  --------#
def InitializeResults(form):
    """

    :param form: 

    """
    BuildResults(form, True, form)
    return


# =====  Radio Button RadVar encoding and decoding =====#
# =====  The value is simply the row * 1000 + col  =====#
def DecodeRadioRowCol(RadValue):
    """

    :param RadValue: 

    """
    container = RadValue // 100000
    row = RadValue // 1000
    col = RadValue % 1000
    return container, row, col


def EncodeRadioRowCol(container, row, col):
    """

    :param container: 
    :param row: 
    :param col: 

    """
    RadValue = container * 100000 + row * 1000 + col
    return RadValue


# -------  FUNCTION BuildResults.  Form exiting so build the results to pass back  ------- #
# format of return values is
# (Button Pressed, input_values)
def BuildResults(form, initialize_only, top_level_form):
    """

    :param form: 
    :param initialize_only: 
    :param top_level_form: 

    """
    # Results for elements are:
    #   TEXT - Nothing
    #   INPUT - Read value from TK
    #   Button - Button Text and position as a Tuple

    # Get the initialized results so we don't have to rebuild
    form.DictionaryKeyCounter = 0
    form.ReturnValuesDictionary = {}
    form.ReturnValuesList = []
    BuildResultsForSubform(form, initialize_only, top_level_form)
    if not top_level_form.LastButtonClickedWasRealtime:
        top_level_form.LastButtonClicked = None
    return form.ReturnValues


def BuildResultsForSubform(form, initialize_only, top_level_form):
    """

    :param form: 
    :param initialize_only: 
    :param top_level_form: 

    """
    button_pressed_text = top_level_form.LastButtonClicked
    for row_num, row in enumerate(form.Rows):
        for col_num, element in enumerate(row):
            if element.Key is not None and WRITE_ONLY_KEY in str(element.Key):
                continue
            value = None
            if element.Type == ELEM_TYPE_COLUMN:
                element.DictionaryKeyCounter = top_level_form.DictionaryKeyCounter
                element.ReturnValuesList = []
                element.ReturnValuesDictionary = {}
                BuildResultsForSubform(element, initialize_only, top_level_form)
                for item in element.ReturnValuesList:
                    AddToReturnList(top_level_form, item)
                if element.UseDictionary:
                    top_level_form.UseDictionary = True
                if element.ReturnValues[0] is not None:  # if a button was clicked
                    button_pressed_text = element.ReturnValues[0]

            if element.Type == ELEM_TYPE_FRAME:
                element.DictionaryKeyCounter = top_level_form.DictionaryKeyCounter
                element.ReturnValuesList = []
                element.ReturnValuesDictionary = {}
                BuildResultsForSubform(element, initialize_only, top_level_form)
                for item in element.ReturnValuesList:
                    AddToReturnList(top_level_form, item)
                if element.UseDictionary:
                    top_level_form.UseDictionary = True
                if element.ReturnValues[0] is not None:  # if a button was clicked
                    button_pressed_text = element.ReturnValues[0]

            if element.Type == ELEM_TYPE_PANE:
                element.DictionaryKeyCounter = top_level_form.DictionaryKeyCounter
                element.ReturnValuesList = []
                element.ReturnValuesDictionary = {}
                BuildResultsForSubform(element, initialize_only, top_level_form)
                for item in element.ReturnValuesList:
                    AddToReturnList(top_level_form, item)
                if element.UseDictionary:
                    top_level_form.UseDictionary = True
                if element.ReturnValues[0] is not None:  # if a button was clicked
                    button_pressed_text = element.ReturnValues[0]

            if element.Type == ELEM_TYPE_TAB_GROUP:
                element.DictionaryKeyCounter = top_level_form.DictionaryKeyCounter
                element.ReturnValuesList = []
                element.ReturnValuesDictionary = {}
                BuildResultsForSubform(element, initialize_only, top_level_form)
                for item in element.ReturnValuesList:
                    AddToReturnList(top_level_form, item)
                if element.UseDictionary:
                    top_level_form.UseDictionary = True
                if element.ReturnValues[0] is not None:  # if a button was clicked
                    button_pressed_text = element.ReturnValues[0]

            if element.Type == ELEM_TYPE_TAB:
                element.DictionaryKeyCounter = top_level_form.DictionaryKeyCounter
                element.ReturnValuesList = []
                element.ReturnValuesDictionary = {}
                BuildResultsForSubform(element, initialize_only, top_level_form)
                for item in element.ReturnValuesList:
                    AddToReturnList(top_level_form, item)
                if element.UseDictionary:
                    top_level_form.UseDictionary = True
                if element.ReturnValues[0] is not None:  # if a button was clicked
                    button_pressed_text = element.ReturnValues[0]

            if not initialize_only:
                if element.Type == ELEM_TYPE_INPUT_TEXT:
                    try:
                        value = element.TKStringVar.get()
                    except:
                        value = ''
                    if not top_level_form.NonBlocking and not element.do_not_clear and not top_level_form.ReturnKeyboardEvents:
                        element.TKStringVar.set('')
                elif element.Type == ELEM_TYPE_INPUT_CHECKBOX:
                    value = element.TKIntVar.get()
                    value = (value != 0)
                elif element.Type == ELEM_TYPE_INPUT_RADIO:
                    RadVar = element.TKIntVar.get()
                    this_rowcol = EncodeRadioRowCol(form.ContainerElemementNumber, row_num, col_num)
                    # this_rowcol = element.EncodedRadioValue       # could use the saved one
                    value = RadVar == this_rowcol
                elif element.Type == ELEM_TYPE_BUTTON:
                    if top_level_form.LastButtonClicked == element.ButtonText:
                        button_pressed_text = top_level_form.LastButtonClicked
                        if element.BType != BUTTON_TYPE_REALTIME:  # Do not clear realtime buttons
                            top_level_form.LastButtonClicked = None
                    if element.BType == BUTTON_TYPE_CALENDAR_CHOOSER:
                        try:
                            value = element.TKCal.selection
                        except:
                            value = None
                    else:
                        try:
                            value = element.TKStringVar.get()
                        except:
                            value = None
                elif element.Type == ELEM_TYPE_INPUT_COMBO:
                    value = element.TKStringVar.get()
                elif element.Type == ELEM_TYPE_INPUT_OPTION_MENU:
                    value = element.TKStringVar.get()
                elif element.Type == ELEM_TYPE_INPUT_LISTBOX:
                    try:
                        items = element.TKListbox.curselection()
                        value = [element.Values[int(item)] for item in items]
                    except:
                        value = ''
                elif element.Type == ELEM_TYPE_INPUT_SPIN:
                    try:
                        value = element.TKStringVar.get()
                    except:
                        value = 0
                elif element.Type == ELEM_TYPE_INPUT_SLIDER:
                    try:
                        value = float(element.TKScale.get())
                    except:
                        value = 0
                elif element.Type == ELEM_TYPE_INPUT_MULTILINE:
                    try:
                        value = element.TKText.get(1.0, tk.END)
                        if not top_level_form.NonBlocking and not element.do_not_clear and not top_level_form.ReturnKeyboardEvents:
                            element.TKText.delete('1.0', tk.END)
                    except:
                        value = None
                elif element.Type == ELEM_TYPE_TAB_GROUP:
                    try:
                        value = element.TKNotebook.tab(element.TKNotebook.index('current'))['text']
                        tab_key = element.FindKeyFromTabName(value)
                        if tab_key is not None:
                            value = tab_key
                    except:
                        value = None
                elif element.Type == ELEM_TYPE_TABLE:
                    value = element.SelectedRows
                elif element.Type == ELEM_TYPE_TREE:
                    value = element.SelectedRows
                elif element.Type == ELEM_TYPE_GRAPH:
                    value = element.ClickPosition
                elif element.Type == ELEM_TYPE_MENUBAR:
                    if element.MenuItemChosen is not None:
                        button_pressed_text = top_level_form.LastButtonClicked = element.MenuItemChosen
                    value = element.MenuItemChosen
                    element.MenuItemChosen = None
                elif element.Type == ELEM_TYPE_BUTTONMENU:
                    value = element.MenuItemChosen
                    element.MenuItemChosen = None

                    # if element.MenuItemChosen is not None:
                    #     button_pressed_text = top_level_form.LastButtonClicked = element.MenuItemChosen
                    # value = element.MenuItemChosen
                    # element.MenuItemChosen = None
            else:
                value = None

            # if an input type element, update the results
            if element.Type != ELEM_TYPE_BUTTON and \
                    element.Type != ELEM_TYPE_TEXT and \
                    element.Type != ELEM_TYPE_IMAGE and \
                    element.Type != ELEM_TYPE_OUTPUT and \
                    element.Type != ELEM_TYPE_PROGRESS_BAR and \
                    element.Type != ELEM_TYPE_COLUMN and \
                    element.Type != ELEM_TYPE_FRAME \
                    and element.Type != ELEM_TYPE_TAB:
                AddToReturnList(form, value)
                AddToReturnDictionary(top_level_form, element, value)
            elif (element.Type == ELEM_TYPE_BUTTON and
                  element.BType == BUTTON_TYPE_CALENDAR_CHOOSER and
                  element.Target == (None, None)) or \
                    (element.Type == ELEM_TYPE_BUTTON and
                     element.BType == BUTTON_TYPE_COLOR_CHOOSER and
                     element.Target == (None, None)) or \
                    (element.Type == ELEM_TYPE_BUTTON
                     and element.Key is not None and
                     (element.BType in (BUTTON_TYPE_SAVEAS_FILE, BUTTON_TYPE_BROWSE_FILE, BUTTON_TYPE_BROWSE_FILES,
                                        BUTTON_TYPE_BROWSE_FOLDER))):
                AddToReturnList(form, value)
                AddToReturnDictionary(top_level_form, element, value)

    # if this is a column, then will fail so need to wrap with tr
    try:
        if form.ReturnKeyboardEvents and form.LastKeyboardEvent is not None:
            button_pressed_text = form.LastKeyboardEvent
            form.LastKeyboardEvent = None
    except:
        pass

    try:
        form.ReturnValuesDictionary.pop(None, None)  # clean up dictionary include None was included
    except:
        pass

    if not form.UseDictionary:
        form.ReturnValues = button_pressed_text, form.ReturnValuesList
    else:
        form.ReturnValues = button_pressed_text, form.ReturnValuesDictionary

    return form.ReturnValues


def FillFormWithValues(form, values_dict):
    """

    :param form: 
    :param values_dict: 

    """
    FillSubformWithValues(form, values_dict)


def FillSubformWithValues(form, values_dict):
    """

    :param form: 
    :param values_dict: 

    """
    for row_num, row in enumerate(form.Rows):
        for col_num, element in enumerate(row):
            value = None
            if element.Type == ELEM_TYPE_COLUMN:
                FillSubformWithValues(element, values_dict)
            if element.Type == ELEM_TYPE_FRAME:
                FillSubformWithValues(element, values_dict)
            if element.Type == ELEM_TYPE_TAB_GROUP:
                FillSubformWithValues(element, values_dict)
            if element.Type == ELEM_TYPE_TAB:
                FillSubformWithValues(element, values_dict)
            try:
                value = values_dict[element.Key]
            except:
                continue
            if element.Type == ELEM_TYPE_INPUT_TEXT:
                element.Update(value)
            elif element.Type == ELEM_TYPE_INPUT_CHECKBOX:
                element.Update(value)
            elif element.Type == ELEM_TYPE_INPUT_RADIO:
                element.Update(value)
            elif element.Type == ELEM_TYPE_INPUT_COMBO:
                element.Update(value)
            elif element.Type == ELEM_TYPE_INPUT_OPTION_MENU:
                element.Update(value)
            elif element.Type == ELEM_TYPE_INPUT_LISTBOX:
                element.SetValue(value)
            elif element.Type == ELEM_TYPE_INPUT_SLIDER:
                element.Update(value)
            elif element.Type == ELEM_TYPE_INPUT_MULTILINE:
                element.Update(value)
            elif element.Type == ELEM_TYPE_INPUT_SPIN:
                element.Update(value)
            elif element.Type == ELEM_TYPE_BUTTON:
                element.Update(value)


def _FindElementFromKeyInSubForm(form, key):
    """

    :param form: 
    :param key: (common_key) Used with window.FindElement and with return values

    """
    for row_num, row in enumerate(form.Rows):
        for col_num, element in enumerate(row):
            if element.Type == ELEM_TYPE_COLUMN:
                matching_elem = _FindElementFromKeyInSubForm(element, key)
                if matching_elem is not None:
                    return matching_elem
            if element.Type == ELEM_TYPE_FRAME:
                matching_elem = _FindElementFromKeyInSubForm(element, key)
                if matching_elem is not None:
                    return matching_elem
            if element.Type == ELEM_TYPE_TAB_GROUP:
                matching_elem = _FindElementFromKeyInSubForm(element, key)
                if matching_elem is not None:
                    return matching_elem
            if element.Type == ELEM_TYPE_PANE:
                matching_elem = _FindElementFromKeyInSubForm(element, key)
                if matching_elem is not None:
                    return matching_elem
            if element.Type == ELEM_TYPE_TAB:
                matching_elem = _FindElementFromKeyInSubForm(element, key)
                if matching_elem is not None:
                    return matching_elem
            if element.Key == key:
                return element


def _FindElementWithFocusInSubForm(form):
    """

    :param form: 

    """
    for row_num, row in enumerate(form.Rows):
        for col_num, element in enumerate(row):
            if element.Type == ELEM_TYPE_COLUMN:
                matching_elem = _FindElementWithFocusInSubForm(element)
                if matching_elem is not None:
                    return matching_elem
            if element.Type == ELEM_TYPE_FRAME:
                matching_elem = _FindElementWithFocusInSubForm(element)
                if matching_elem is not None:
                    return matching_elem
            if element.Type == ELEM_TYPE_TAB_GROUP:
                matching_elem = _FindElementWithFocusInSubForm(element)
                if matching_elem is not None:
                    return matching_elem
            if element.Type == ELEM_TYPE_TAB:
                matching_elem = _FindElementWithFocusInSubForm(element)
                if matching_elem is not None:
                    return matching_elem
            if element.Type == ELEM_TYPE_INPUT_TEXT:
                if element.TKEntry is not None:
                    if element.TKEntry is element.TKEntry.focus_get():
                        return element
            if element.Type == ELEM_TYPE_INPUT_MULTILINE:
                if element.TKText is not None:
                    if element.TKText is element.TKText.focus_get():
                        return element
            if element.Type == ELEM_TYPE_BUTTON:
                if element.TKButton is not None:
                    if element.TKButton is element.TKButton.focus_get():
                        return element


if sys.version_info[0] >= 3:
    def AddMenuItem(top_menu, sub_menu_info, element, is_sub_menu=False, skip=False):
        """

        :param top_menu: 
        :param sub_menu_info: 
        :param element: 
        :param is_sub_menu:  (Default value = False)
        :param skip:  (Default value = False)

        """
        return_val = None
        if type(sub_menu_info) is str:
            if not is_sub_menu and not skip:
                # print(f'Adding command {sub_menu_info}')
                pos = sub_menu_info.find('&')
                if pos != -1:
                    if pos == 0 or sub_menu_info[pos - 1] != "\\":
                        sub_menu_info = sub_menu_info[:pos] + sub_menu_info[pos + 1:]
                if sub_menu_info == '---':
                    top_menu.add('separator')
                else:
                    try:
                        item_without_key = sub_menu_info[:sub_menu_info.index(MENU_KEY_SEPARATOR)]
                    except:
                        item_without_key = sub_menu_info

                    if item_without_key[0] == MENU_DISABLED_CHARACTER:
                        top_menu.add_command(label=item_without_key[len(MENU_DISABLED_CHARACTER):], underline=pos,
                                             command=lambda: element._MenuItemChosenCallback(sub_menu_info))
                        top_menu.entryconfig(item_without_key[len(MENU_DISABLED_CHARACTER):], state='disabled')
                    else:
                        top_menu.add_command(label=item_without_key, underline=pos,
                                             command=lambda: element._MenuItemChosenCallback(sub_menu_info))
        else:
            i = 0
            while i < (len(sub_menu_info)):
                item = sub_menu_info[i]
                if i != len(sub_menu_info) - 1:
                    if type(sub_menu_info[i + 1]) == list:
                        new_menu = tk.Menu(top_menu, tearoff=element.Tearoff)
                        return_val = new_menu
                        pos = sub_menu_info[i].find('&')
                        if pos != -1:
                            if pos == 0 or sub_menu_info[i][pos - 1] != "\\":
                                sub_menu_info[i] = sub_menu_info[i][:pos] + sub_menu_info[i][pos + 1:]
                        if sub_menu_info[i][0] == MENU_DISABLED_CHARACTER:
                            top_menu.add_cascade(label=sub_menu_info[i][len(MENU_DISABLED_CHARACTER):], menu=new_menu,
                                                 underline=pos, state='disabled')
                        else:
                            top_menu.add_cascade(label=sub_menu_info[i], menu=new_menu, underline=pos)
                        AddMenuItem(new_menu, sub_menu_info[i + 1], element, is_sub_menu=True)
                        i += 1  # skip the next one
                    else:
                        AddMenuItem(top_menu, item, element)
                else:
                    AddMenuItem(top_menu, item, element)
                i += 1
        return return_val
else:
    def AddMenuItem(top_menu, sub_menu_info, element, is_sub_menu=False, skip=False):
        """

        :param top_menu: 
        :param sub_menu_info: 
        :param element: 
        :param is_sub_menu:  (Default value = False)
        :param skip:  (Default value = False)

        """
        if not isinstance(sub_menu_info, list):
            if not is_sub_menu and not skip:
                # print(f'Adding command {sub_menu_info}')
                pos = sub_menu_info.find('&')
                if pos != -1:
                    if pos == 0 or sub_menu_info[pos - 1] != "\\":
                        sub_menu_info = sub_menu_info[:pos] + sub_menu_info[pos + 1:]
                if sub_menu_info == '---':
                    top_menu.add('separator')
                else:
                    try:
                        item_without_key = sub_menu_info[:sub_menu_info.index(MENU_KEY_SEPARATOR)]
                    except:
                        item_without_key = sub_menu_info

                    if item_without_key[0] == MENU_DISABLED_CHARACTER:
                        top_menu.add_command(label=item_without_key[len(MENU_DISABLED_CHARACTER):], underline=pos,
                                             command=lambda: element._MenuItemChosenCallback(sub_menu_info))
                        top_menu.entryconfig(item_without_key[len(MENU_DISABLED_CHARACTER):], state='disabled')
                    else:
                        top_menu.add_command(label=item_without_key, underline=pos,
                                             command=lambda: element._MenuItemChosenCallback(sub_menu_info))
        else:
            i = 0
            while i < (len(sub_menu_info)):
                item = sub_menu_info[i]
                if i != len(sub_menu_info) - 1:
                    if isinstance(sub_menu_info[i + 1], list):
                        new_menu = tk.Menu(top_menu, tearoff=element.Tearoff)
                        pos = sub_menu_info[i].find('&')
                        if pos != -1:
                            if pos == 0 or sub_menu_info[i][pos - 1] != "\\":
                                sub_menu_info[i] = sub_menu_info[i][:pos] + sub_menu_info[i][pos + 1:]
                        if sub_menu_info[i][0] == MENU_DISABLED_CHARACTER:
                            top_menu.add_cascade(label=sub_menu_info[i][len(MENU_DISABLED_CHARACTER):], menu=new_menu,
                                                 underline=pos, state='disabled')
                        else:
                            top_menu.add_cascade(label=sub_menu_info[i], menu=new_menu, underline=pos)
                        AddMenuItem(new_menu, sub_menu_info[i + 1], element, is_sub_menu=True)
                        i += 1  # skip the next one
                    else:
                        AddMenuItem(top_menu, item, element)
                else:
                    AddMenuItem(top_menu, item, element)
                i += 1

# 888    888      d8b          888
# 888    888      Y8P          888
# 888    888                   888
# 888888 888  888 888 88888b.  888888  .d88b.  888d888
# 888    888 .88P 888 888 "88b 888    d8P  Y8b 888P"
# 888    888888K  888 888  888 888    88888888 888
# Y88b.  888 "88b 888 888  888 Y88b.  Y8b.     888
#  "Y888 888  888 888 888  888  "Y888  "Y8888  888

# My crappy tkinter code starts here

"""
         )
        (
          ,
       ___)\
      (_____)
      (_______)

"""


# ========================   TK CODE STARTS HERE ========================================= #

def PackFormIntoFrame(form, containing_frame, toplevel_form):
    """

    :param form: 
    :param containing_frame: 
    :param toplevel_form: 

    """
    def CharWidthInPixels():
        """ """
        return tkinter.font.Font().measure('A')  # single character width

    border_depth = toplevel_form.BorderDepth if toplevel_form.BorderDepth is not None else DEFAULT_BORDER_WIDTH
    # --------------------------------------------------------------------------- #
    # ****************  Use FlexForm to build the tkinter window ********** ----- #
    # Building is done row by row.                                                #
    # --------------------------------------------------------------------------- #
    focus_set = False
    ######################### LOOP THROUGH ROWS #########################
    # *********** -------  Loop through ROWS  ------- ***********#
    for row_num, flex_row in enumerate(form.Rows):
        ######################### LOOP THROUGH ELEMENTS ON ROW #########################
        # *********** -------  Loop through ELEMENTS  ------- ***********#
        # *********** Make TK Row                             ***********#
        tk_row_frame = tk.Frame(containing_frame)
        row_should_expand = False
        for col_num, element in enumerate(flex_row):
            element.ParentForm = toplevel_form  # save the button's parent form object
            if toplevel_form.Font and (element.Font == DEFAULT_FONT or not element.Font):
                font = toplevel_form.Font
            elif element.Font is not None:
                font = element.Font
            else:
                font = DEFAULT_FONT
            # -------  Determine Auto-Size setting on a cascading basis ------- #
            if element.AutoSizeText is not None:  # if element overide
                auto_size_text = element.AutoSizeText
            elif toplevel_form.AutoSizeText is not None:  # if form override
                auto_size_text = toplevel_form.AutoSizeText
            else:
                auto_size_text = DEFAULT_AUTOSIZE_TEXT
            element_type = element.Type
            # Set foreground color
            text_color = element.TextColor
            elementpad = element.Pad if element.Pad is not None else toplevel_form.ElementPadding
            # Determine Element size
            element_size = element.Size
            if (element_size == (None, None) and element_type not in (
                    ELEM_TYPE_BUTTON, ELEM_TYPE_BUTTONMENU)):  # user did not specify a size
                element_size = toplevel_form.DefaultElementSize
            elif (element_size == (None, None) and element_type in (ELEM_TYPE_BUTTON, ELEM_TYPE_BUTTONMENU)):
                element_size = toplevel_form.DefaultButtonElementSize
            else:
                auto_size_text = False  # if user has specified a size then it shouldn't autosize
            # -------------------------  COLUMN element  ------------------------- #
            if element_type == ELEM_TYPE_COLUMN:
                if element.Scrollable:
                    element.TKColFrame = element.Widget = TkScrollableFrame(tk_row_frame,
                                                                            element.VerticalScrollOnly)  # do not use yet!  not working
                    PackFormIntoFrame(element, element.TKColFrame.TKFrame, toplevel_form)
                    element.TKColFrame.TKFrame.update()
                    if element.Size == (None, None):  # if no size specified, use column width x column height/2
                        element.TKColFrame.canvas.config(width=element.TKColFrame.TKFrame.winfo_reqwidth(),
                                                         height=element.TKColFrame.TKFrame.winfo_reqheight() / 2)
                    else:
                        element.TKColFrame.canvas.config(width=element.Size[0], height=element.Size[1])

                    if not element.BackgroundColor in (None, COLOR_SYSTEM_DEFAULT):
                        element.TKColFrame.canvas.config(background=element.BackgroundColor)
                        element.TKColFrame.TKFrame.config(background=element.BackgroundColor, borderwidth=0,
                                                          highlightthickness=0)
                        element.TKColFrame.config(background=element.BackgroundColor, borderwidth=0,
                                                  highlightthickness=0)
                else:
                    if element.Size != (None, None):
                        element.TKColFrame = TkFixedFrame(tk_row_frame)
                        PackFormIntoFrame(element, element.TKColFrame.TKFrame, toplevel_form)
                        element.TKColFrame.TKFrame.update()
                        if element.Size[1] is not None:
                            element.TKColFrame.canvas.config(height=element.Size[1])
                        elif element.Size[0] is not None:
                            element.TKColFrame.canvas.config(width=element.Size[0])
                    else:
                        element.TKColFrame = tk.Frame(tk_row_frame)
                        PackFormIntoFrame(element, element.TKColFrame, toplevel_form)

                element.TKColFrame.pack(side=tk.LEFT, padx=elementpad[0], pady=elementpad[1], expand=True, fill='both')
                if element.Visible is False:
                    element.TKColFrame.pack_forget()

                element.TKColFrame = element.TKColFrame
                if element.BackgroundColor != COLOR_SYSTEM_DEFAULT and element.BackgroundColor is not None:
                    element.TKColFrame.configure(background=element.BackgroundColor,
                                                 highlightbackground=element.BackgroundColor,
                                                 highlightcolor=element.BackgroundColor)
                if element.RightClickMenu or toplevel_form.RightClickMenu:
                    menu = element.RightClickMenu or toplevel_form.RightClickMenu
                    top_menu = tk.Menu(toplevel_form.TKroot, tearoff=False)
                    AddMenuItem(top_menu, menu[1], element)
                    element.TKRightClickMenu = top_menu
                    element.TKColFrame.bind('<Button-3>', element._RightClickMenuCallback)
            # -------------------------  Pane element  ------------------------- #
            if element_type == ELEM_TYPE_PANE:
                bd = element.BorderDepth if element.BorderDepth is not None else border_depth
                element.PanedWindow = element.Widget = tk.PanedWindow(tk_row_frame,
                                                                      orient=tk.VERTICAL if element.Orientation.startswith(
                                                                          'v') else tk.HORIZONTAL,
                                                                      borderwidth=bd,
                                                                      bd=bd,
                                                                      )
                if element.Relief is not None:
                    element.PanedWindow.configure(relief=element.Relief)
                element.PanedWindow.configure(handlesize=element.HandleSize)
                if element.ShowHandle:
                    element.PanedWindow.config(showhandle=True)
                if element.Size != (None, None):
                    element.PanedWindow.config(width=element.Size[0], height=element.Size[1])
                if element.BackgroundColor is not None and element.BackgroundColor != COLOR_SYSTEM_DEFAULT:
                    element.PanedWindow.configure(background=element.BackgroundColor)
                for pane in element.PaneList:
                    pane.TKColFrame = tk.Frame(element.PanedWindow)
                    pane.ParentPanedWindow = element.PanedWindow
                    PackFormIntoFrame(pane, pane.TKColFrame, toplevel_form)
                    if pane.Visible:
                        element.PanedWindow.add(pane.TKColFrame)
                    if pane.BackgroundColor != COLOR_SYSTEM_DEFAULT and pane.BackgroundColor is not None:
                        pane.TKColFrame.configure(background=pane.BackgroundColor,
                                                  highlightbackground=pane.BackgroundColor,
                                                  highlightcolor=pane.BackgroundColor)

                element.PanedWindow.pack(side=tk.LEFT, padx=elementpad[0], pady=elementpad[1], expand=True, fill='both')
                if element.Visible is False:
                    element.PanedWindow.pack_forget()
            # -------------------------  TEXT element  ------------------------- #
            elif element_type == ELEM_TYPE_TEXT:
                # auto_size_text = element.AutoSizeText
                element = element  # type: Text
                display_text = element.DisplayText  # text to display
                if auto_size_text is False:
                    width, height = element_size
                else:
                    lines = display_text.split('\n')
                    max_line_len = max([len(l) for l in lines])
                    num_lines = len(lines)
                    if max_line_len > element_size[0]:  # if text exceeds element size, the will have to wrap
                        width = element_size[0]
                    else:
                        width = max_line_len
                    height = num_lines
                # ---===--- LABEL widget create and place --- #
                stringvar = tk.StringVar()
                element.TKStringVar = stringvar
                stringvar.set(str(display_text))
                if auto_size_text:
                    width = 0
                if element.Justification is not None:
                    justification = element.Justification
                elif toplevel_form.TextJustification is not None:
                    justification = toplevel_form.TextJustification
                else:
                    justification = DEFAULT_TEXT_JUSTIFICATION
                justify = tk.LEFT if justification == 'left' else tk.CENTER if justification == 'center' else tk.RIGHT
                anchor = tk.NW if justification == 'left' else tk.N if justification == 'center' else tk.NE

                tktext_label = element.Widget = tk.Label(tk_row_frame, textvariable=stringvar, width=width,
                                                         height=height, justify=justify, bd=border_depth, font=font)
                # Set wrap-length for text (in PIXELS) == PAIN IN THE ASS
                wraplen = tktext_label.winfo_reqwidth()  # width of widget in Pixels
                if not auto_size_text and height == 1:   # if just 1 line high, ensure no wrap happens
                    wraplen = 0
                # print(f'Text wraplen = {wraplen} wxh = {width} x {height}')
                # print(f'Len = {len(display_text)} Text = {str(display_text)}')
                tktext_label.configure(anchor=anchor, wraplen=wraplen)  # set wrap to width of widget
                if element.Relief is not None:
                    tktext_label.configure(relief=element.Relief)
                if element.BackgroundColor is not None and element.BackgroundColor != COLOR_SYSTEM_DEFAULT:
                    tktext_label.configure(background=element.BackgroundColor)
                if element.TextColor != COLOR_SYSTEM_DEFAULT and element.TextColor is not None:
                    tktext_label.configure(fg=element.TextColor)
                tktext_label.pack(side=tk.LEFT, padx=elementpad[0], pady=elementpad[1])
                if element.Visible is False:
                    tktext_label.pack_forget()
                element.TKText = tktext_label
                if element.ClickSubmits:
                    tktext_label.bind('<Button-1>', element._TextClickedHandler)
                if element.Tooltip is not None:
                    element.TooltipObject = ToolTip(element.TKText, text=element.Tooltip, timeout=DEFAULT_TOOLTIP_TIME)
                if element.RightClickMenu or toplevel_form.RightClickMenu:
                    menu = element.RightClickMenu or toplevel_form.RightClickMenu
                    top_menu = tk.Menu(toplevel_form.TKroot, tearoff=False)
                    AddMenuItem(top_menu, menu[1], element)
                    element.TKRightClickMenu = top_menu
                    tktext_label.bind('<Button-3>', element._RightClickMenuCallback)
            # -------------------------  BUTTON element  ------------------------- #
            elif element_type == ELEM_TYPE_BUTTON:
                element = element  # type: Button
                stringvar = tk.StringVar()
                element.TKStringVar = stringvar
                element.Location = (row_num, col_num)
                btext = element.ButtonText
                btype = element.BType
                if element.AutoSizeButton is not None:
                    auto_size = element.AutoSizeButton
                else:
                    auto_size = toplevel_form.AutoSizeButtons
                if auto_size is False or element.Size[0] is not None:
                    width, height = element_size
                else:
                    width = 0
                    height = toplevel_form.DefaultButtonElementSize[1]
                if element.ButtonColor != (None, None) and element.ButtonColor != DEFAULT_BUTTON_COLOR:
                    bc = element.ButtonColor
                elif toplevel_form.ButtonColor != (None, None) and toplevel_form.ButtonColor != DEFAULT_BUTTON_COLOR:
                    bc = toplevel_form.ButtonColor
                else:
                    bc = DEFAULT_BUTTON_COLOR
                border_depth = element.BorderWidth
                if btype != BUTTON_TYPE_REALTIME:
                    tkbutton = element.Widget = tk.Button(tk_row_frame, text=btext, width=width, height=height,
                                                          command=element.ButtonCallBack, justify=tk.LEFT,
                                                          bd=border_depth, font=font)
                else:
                    tkbutton = element.Widget = tk.Button(tk_row_frame, text=btext, width=width, height=height,
                                                          justify=tk.LEFT,
                                                          bd=border_depth, font=font)
                    tkbutton.bind('<ButtonRelease-1>', element.ButtonReleaseCallBack)
                    tkbutton.bind('<ButtonPress-1>', element.ButtonPressCallBack)
                if bc != (None, None) and bc != COLOR_SYSTEM_DEFAULT and bc[1] != COLOR_SYSTEM_DEFAULT:
                    tkbutton.config(foreground=bc[0], background=bc[1], activebackground=bc[1])
                elif bc[1] == COLOR_SYSTEM_DEFAULT:
                    tkbutton.config(foreground=bc[0])
                if border_depth == 0:
                    tkbutton.config(relief=tk.FLAT)
                    tkbutton.config(highlightthickness=0)
                element.TKButton = tkbutton  # not used yet but save the TK button in case
                wraplen = tkbutton.winfo_reqwidth()  # width of widget in Pixels
                if element.ImageFilename:  # if button has an image on it
                    tkbutton.config(highlightthickness=0)
                    photo = tk.PhotoImage(file=element.ImageFilename)
                    if element.ImageSubsample:
                        photo = photo.subsample(element.ImageSubsample)
                    if element.ImageSize != (None, None):
                        width, height = element.ImageSize
                    else:
                        width, height = photo.width(), photo.height()
                    tkbutton.config(image=photo, compound=tk.CENTER, width=width, height=height)
                    tkbutton.image = photo
                if element.ImageData:  # if button has an image on it
                    tkbutton.config(highlightthickness=0)
                    photo = tk.PhotoImage(data=element.ImageData)
                    if element.ImageSubsample:
                        photo = photo.subsample(element.ImageSubsample)
                    if element.ImageSize != (None, None):
                        width, height = element.ImageSize
                    else:
                        width, height = photo.width(), photo.height()
                    tkbutton.config(image=photo, compound=tk.CENTER, width=width, height=height)
                    tkbutton.image = photo
                if width != 0:
                    tkbutton.configure(wraplength=wraplen + 10)  # set wrap to width of widget
                tkbutton.pack(side=tk.LEFT, padx=elementpad[0], pady=elementpad[1])
                if element.Visible is False:
                    tkbutton.pack_forget()
                if element.BindReturnKey:
                    element.TKButton.bind('<Return>', element._ReturnKeyHandler)
                if element.Focus is True or (toplevel_form.UseDefaultFocus and not focus_set):
                    focus_set = True
                    element.TKButton.bind('<Return>', element._ReturnKeyHandler)
                    element.TKButton.focus_set()
                    toplevel_form.TKroot.focus_force()
                if element.Disabled == True:
                    element.TKButton['state'] = 'disabled'
                if element.Tooltip is not None:
                    element.TooltipObject = ToolTip(element.TKButton, text=element.Tooltip,
                                                    timeout=DEFAULT_TOOLTIP_TIME)
            # -------------------------  BUTTONMENU element  ------------------------- #
            elif element_type == ELEM_TYPE_BUTTONMENU:
                element.Location = (row_num, col_num)
                btext = element.ButtonText
                if element.AutoSizeButton is not None:
                    auto_size = element.AutoSizeButton
                else:
                    auto_size = toplevel_form.AutoSizeButtons
                if auto_size is False or element.Size[0] is not None:
                    width, height = element_size
                else:
                    width = 0
                    height = toplevel_form.DefaultButtonElementSize[1]
                if element.ButtonColor != (None, None) and element.ButtonColor != DEFAULT_BUTTON_COLOR:
                    bc = element.ButtonColor
                elif toplevel_form.ButtonColor != (None, None) and toplevel_form.ButtonColor != DEFAULT_BUTTON_COLOR:
                    bc = toplevel_form.ButtonColor
                else:
                    bc = DEFAULT_BUTTON_COLOR
                border_depth = element.BorderWidth
                tkbutton = element.Widget = tk.Menubutton(tk_row_frame, text=btext, width=width, height=height,
                                                          justify=tk.LEFT, bd=border_depth, font=font)
                element.TKButtonMenu = tkbutton
                if bc != (None, None) and bc != COLOR_SYSTEM_DEFAULT and bc[1] != COLOR_SYSTEM_DEFAULT:
                    tkbutton.config(foreground=bc[0], background=bc[1], activebackground=bc[1])
                elif bc[1] == COLOR_SYSTEM_DEFAULT:
                    tkbutton.config(foreground=bc[0])
                if border_depth == 0:
                    tkbutton.config(relief=tk.FLAT)
                    tkbutton.config(highlightthickness=0)
                element.TKButton = tkbutton  # not used yet but save the TK button in case
                wraplen = tkbutton.winfo_reqwidth()  # width of widget in Pixels
                if element.ImageFilename:  # if button has an image on it
                    tkbutton.config(highlightthickness=0)
                    photo = tk.PhotoImage(file=element.ImageFilename)
                    if element.ImageSize != (None, None):
                        width, height = element.ImageSize
                        if element.ImageSubsample:
                            photo = photo.subsample(element.ImageSubsample)
                    else:
                        width, height = photo.width(), photo.height()
                    tkbutton.config(image=photo, compound=tk.CENTER, width=width, height=height)
                    tkbutton.image = photo
                if element.ImageData:  # if button has an image on it
                    tkbutton.config(highlightthickness=0)
                    photo = tk.PhotoImage(data=element.ImageData)
                    if element.ImageSize != (None, None):
                        width, height = element.ImageSize
                        if element.ImageSubsample:
                            photo = photo.subsample(element.ImageSubsample)
                    else:
                        width, height = photo.width(), photo.height()
                    tkbutton.config(image=photo, compound=tk.CENTER, width=width, height=height)
                    tkbutton.image = photo
                if width != 0:
                    tkbutton.configure(wraplength=wraplen + 10)  # set wrap to width of widget
                tkbutton.pack(side=tk.LEFT, padx=elementpad[0], pady=elementpad[1])

                menu_def = element.MenuDefinition

                top_menu = tk.Menu(tkbutton, tearoff=False)
                AddMenuItem(top_menu, menu_def[1], element)

                tkbutton.configure(menu=top_menu)

                if element.Visible is False:
                    tkbutton.pack_forget()
                if element.Disabled == True:
                    element.TKButton['state'] = 'disabled'
                if element.Tooltip is not None:
                    element.TooltipObject = ToolTip(element.TKButton, text=element.Tooltip,
                                                    timeout=DEFAULT_TOOLTIP_TIME)


            # -------------------------  INPUT element  ------------------------- #
            elif element_type == ELEM_TYPE_INPUT_TEXT:
                element = element  # type: InputText
                default_text = element.DefaultText
                element.TKStringVar = tk.StringVar()
                element.TKStringVar.set(default_text)
                show = element.PasswordCharacter if element.PasswordCharacter else ""
                if element.Justification is not None:
                    justification = element.Justification
                else:
                    justification = DEFAULT_TEXT_JUSTIFICATION
                justify = tk.LEFT if justification == 'left' else tk.CENTER if justification == 'center' else tk.RIGHT
                # anchor = tk.NW if justification == 'left' else tk.N if justification == 'center' else tk.NE
                element.TKEntry = element.Widget = tk.Entry(tk_row_frame, width=element_size[0],
                                                            textvariable=element.TKStringVar, bd=border_depth,
                                                            font=font, show=show, justify=justify)
                if element.ChangeSubmits:
                    element.TKEntry.bind('<Key>', element._KeyboardHandler)
                element.TKEntry.bind('<Return>', element._ReturnKeyHandler)
                if element.BackgroundColor is not None and element.BackgroundColor != COLOR_SYSTEM_DEFAULT:
                    element.TKEntry.configure(background=element.BackgroundColor)
                if text_color is not None and text_color != COLOR_SYSTEM_DEFAULT:
                    element.TKEntry.configure(fg=text_color)
                element.TKEntry.pack(side=tk.LEFT, padx=elementpad[0], pady=elementpad[1], expand=True, fill='x')
                if element.Visible is False:
                    element.TKEntry.pack_forget()
                if element.Focus is True or (toplevel_form.UseDefaultFocus and not focus_set):
                    focus_set = True
                    element.TKEntry.focus_set()
                if element.Disabled:
                    element.TKEntry['state'] = 'readonly'
                if element.Tooltip is not None:
                    element.TooltipObject = ToolTip(element.TKEntry, text=element.Tooltip, timeout=DEFAULT_TOOLTIP_TIME)
                if element.RightClickMenu or toplevel_form.RightClickMenu:
                    menu = element.RightClickMenu or toplevel_form.RightClickMenu
                    top_menu = tk.Menu(toplevel_form.TKroot, tearoff=False)
                    AddMenuItem(top_menu, menu[1], element)
                    element.TKRightClickMenu = top_menu
                    element.TKEntry.bind('<Button-3>', element._RightClickMenuCallback)
            # -------------------------  COMBOBOX element  ------------------------- #
            elif element_type == ELEM_TYPE_INPUT_COMBO:
                max_line_len = max([len(str(l)) for l in element.Values]) if len(element.Values) else 0
                if auto_size_text is False:
                    width = element_size[0]
                else:
                    width = max_line_len
                element.TKStringVar = tk.StringVar()
                style_name = 'TCombobox'
                if element.TextColor is not None and element.TextColor != COLOR_SYSTEM_DEFAULT:
                    # Creates 1 style per Text Color/ Background Color combination
                    style_name = element.TextColor + element.BackgroundColor + '.TCombobox'
                    # print(style_name)
                    combostyle = ttk.Style()

                    # Creates a unique name for each field element(Sure there is a better way to do this)

                    unique_field = str(element.Key) + '.TCombobox.field'

                    # unique_field = str(time.time()).replace('.', '') + str(element.Key) + '.TCombobox.field'

                    # unique_field = str(time.time()).replace('.','') + '.TCombobox.field'
                    # unique_field = str(datetime.datetime.today().timestamp()).replace('.','') + '.TCombobox.field'
                    # unique_field = str(randint(1,50000000)) + '.TCombobox.field'

                    # print(unique_field)
                    # Clones over the TCombobox.field element from the "alt" theme.
                    # This is what will allow us to change the background color without altering the whole programs theme
                    combostyle.element_create(unique_field, "from", "alt")

                    # Create widget layout using cloned "alt" field
                    combostyle.layout(style_name, [
                        (unique_field, {'children': [('Combobox.downarrow', {'side': 'right', 'sticky': 'ns'}),
                                                     ('Combobox.padding',
                                                      {'children': [('Combobox.focus',
                                                                     {'children': [('Combobox.textarea',
                                                                                    {'sticky': 'nswe'})],
                                                                      'expand': '1',
                                                                      'sticky': 'nswe'})],
                                                       'expand': '1',
                                                       'sticky': 'nswe'})],
                                        'sticky': 'nswe'})])

                    # Copy default TCombobox settings
                    # Getting an error on this line of code
                    # combostyle.configure(style_name, *combostyle.configure("TCombobox"))

                    # Set individual widget options
                    combostyle.configure(style_name, foreground=element.TextColor)
                    combostyle.configure(style_name, selectbackground='gray70')
                    combostyle.configure(style_name, fieldbackground=element.BackgroundColor)
                    combostyle.configure(style_name, selectforeground=element.TextColor)

                element.TKCombo = element.Widget = ttk.Combobox(tk_row_frame, width=width,
                                                                textvariable=element.TKStringVar, font=font,
                                                                style=style_name)
                if element.Size[1] != 1 and element.Size[1] is not None:
                    element.TKCombo.configure(height=element.Size[1])
                element.TKCombo['values'] = element.Values

                element.TKCombo.pack(side=tk.LEFT, padx=elementpad[0], pady=elementpad[1])
                if element.Visible is False:
                    element.TKCombo.pack_forget()
                if element.DefaultValue:
                    for i, v in enumerate(element.Values):
                        if v == element.DefaultValue:
                            element.TKCombo.current(i)
                            break
                elif element.Values:
                    element.TKCombo.current(0)
                if element.ChangeSubmits:
                    element.TKCombo.bind('<<ComboboxSelected>>', element._ComboboxSelectHandler)
                if element.Readonly:
                    element.TKCombo['state'] = 'readonly'
                if element.Disabled is True:  # note overrides readonly if disabled
                    element.TKCombo['state'] = 'disabled'
                if element.Tooltip is not None:
                    element.TooltipObject = ToolTip(element.TKCombo, text=element.Tooltip, timeout=DEFAULT_TOOLTIP_TIME)
            # -------------------------  OPTION MENU Element (Like ComboBox but different) element  ------------------------- #
            elif element_type == ELEM_TYPE_INPUT_OPTION_MENU:
                max_line_len = max([len(str(l)) for l in element.Values])
                if auto_size_text is False:
                    width = element_size[0]
                else:
                    width = max_line_len
                element.TKStringVar = tk.StringVar()
                default = element.DefaultValue if element.DefaultValue else element.Values[0]
                element.TKStringVar.set(default)
                element.TKOptionMenu = element.Widget = tk.OptionMenu(tk_row_frame, element.TKStringVar,
                                                                      *element.Values)
                element.TKOptionMenu.config(highlightthickness=0, font=font, width=width)
                element.TKOptionMenu.config(borderwidth=border_depth)
                if element.BackgroundColor is not None and element.BackgroundColor != COLOR_SYSTEM_DEFAULT:
                    element.TKOptionMenu.configure(background=element.BackgroundColor)
                if element.TextColor != COLOR_SYSTEM_DEFAULT and element.TextColor is not None:
                    element.TKOptionMenu.configure(fg=element.TextColor)
                element.TKOptionMenu.pack(side=tk.LEFT, padx=elementpad[0], pady=elementpad[1])
                if element.Visible is False:
                    element.TKOptionMenu.pack_forget()
                if element.Disabled == True:
                    element.TKOptionMenu['state'] = 'disabled'
                if element.Tooltip is not None:
                    element.TooltipObject = ToolTip(element.TKOptionMenu, text=element.Tooltip,
                                                    timeout=DEFAULT_TOOLTIP_TIME)
            # -------------------------  LISTBOX element  ------------------------- #
            elif element_type == ELEM_TYPE_INPUT_LISTBOX:
                element = element  # type: Listbox
                max_line_len = max([len(str(l)) for l in element.Values]) if len(element.Values) else 0
                if auto_size_text is False:
                    width = element_size[0]
                else:
                    width = max_line_len
                listbox_frame = tk.Frame(tk_row_frame)
                element.TKStringVar = tk.StringVar()
                element.TKListbox = element.Widget = tk.Listbox(listbox_frame, height=element_size[1], width=width,
                                                                selectmode=element.SelectMode, font=font,
                                                                exportselection=False)
                for index, item in enumerate(element.Values):
                    element.TKListbox.insert(tk.END, item)
                    if element.DefaultValues is not None and item in element.DefaultValues:
                        element.TKListbox.selection_set(index)
                if element.BackgroundColor is not None and element.BackgroundColor != COLOR_SYSTEM_DEFAULT:
                    element.TKListbox.configure(background=element.BackgroundColor)
                if text_color is not None and text_color != COLOR_SYSTEM_DEFAULT:
                    element.TKListbox.configure(fg=text_color)
                if element.ChangeSubmits:
                    element.TKListbox.bind('<<ListboxSelect>>', element._ListboxSelectHandler)
                element.vsb = tk.Scrollbar(listbox_frame, orient="vertical", command=element.TKListbox.yview)
                element.TKListbox.configure(yscrollcommand=element.vsb.set)
                element.TKListbox.pack(side=tk.LEFT)
                element.vsb.pack(side=tk.LEFT, fill='y')
                listbox_frame.pack(side=tk.LEFT, padx=elementpad[0], pady=elementpad[1])
                if element.Visible is False:
                    listbox_frame.pack_forget()
                    element.vsb.pack_forget()
                if element.BindReturnKey:
                    element.TKListbox.bind('<Return>', element._ListboxSelectHandler)
                    element.TKListbox.bind('<Double-Button-1>', element._ListboxSelectHandler)
                if element.Disabled == True:
                    element.TKListbox['state'] = 'disabled'
                if element.Tooltip is not None:
                    element.TooltipObject = ToolTip(element.TKListbox, text=element.Tooltip,
                                                    timeout=DEFAULT_TOOLTIP_TIME)
                if element.RightClickMenu or toplevel_form.RightClickMenu:
                    menu = element.RightClickMenu or toplevel_form.RightClickMenu
                    top_menu = tk.Menu(toplevel_form.TKroot, tearoff=False)
                    AddMenuItem(top_menu, menu[1], element)
                    element.TKRightClickMenu = top_menu
                    element.TKListbox.bind('<Button-3>', element._RightClickMenuCallback)
            # -------------------------  MULTILINE element  ------------------------- #
            elif element_type == ELEM_TYPE_INPUT_MULTILINE:
                element = element  # type: Multiline
                default_text = element.DefaultText
                width, height = element_size
                border_depth = element.BorderWidth
                element.TKText = element.Widget = tk.scrolledtext.ScrolledText(tk_row_frame, width=width, height=height,
                                                                               wrap='word', bd=border_depth, font=font,
                                                                               relief=RELIEF_SUNKEN)
                element.TKText.insert(1.0, default_text)  # set the default text
                if element.BackgroundColor is not None and element.BackgroundColor != COLOR_SYSTEM_DEFAULT:
                    element.TKText.configure(background=element.BackgroundColor)
                if DEFAULT_SCROLLBAR_COLOR not in (None, COLOR_SYSTEM_DEFAULT):
                    element.TKText.vbar.config(troughcolor=DEFAULT_SCROLLBAR_COLOR)
                element.TKText.pack(side=tk.LEFT, padx=elementpad[0], pady=elementpad[1], expand=True, fill='both')
                if element.Visible is False:
                    element.TKText.pack_forget()
                if element.ChangeSubmits:
                    element.TKText.bind('<Key>', element._KeyboardHandler)
                if element.EnterSubmits:
                    element.TKText.bind('<Return>', element._ReturnKeyHandler)
                if element.Focus is True or (toplevel_form.UseDefaultFocus and not focus_set):
                    focus_set = True
                    element.TKText.focus_set()
                if text_color is not None and text_color != COLOR_SYSTEM_DEFAULT:
                    element.TKText.configure(fg=text_color)
                if element.Disabled == True:
                    element.TKText['state'] = 'disabled'
                if element.Tooltip is not None:
                    element.TooltipObject = ToolTip(element.TKText, text=element.Tooltip, timeout=DEFAULT_TOOLTIP_TIME)
                if element.RightClickMenu or toplevel_form.RightClickMenu:
                    menu = element.RightClickMenu or toplevel_form.RightClickMenu
                    top_menu = tk.Menu(toplevel_form.TKroot, tearoff=False)
                    AddMenuItem(top_menu, menu[1], element)
                    element.TKRightClickMenu = top_menu
                    element.TKText.bind('<Button-3>', element._RightClickMenuCallback)
                row_should_expand = True
            # -------------------------  CHECKBOX element  ------------------------- #
            elif element_type == ELEM_TYPE_INPUT_CHECKBOX:
                width = 0 if auto_size_text else element_size[0]
                default_value = element.InitialState
                element.TKIntVar = tk.IntVar()
                element.TKIntVar.set(default_value if default_value is not None else 0)
                if element.ChangeSubmits:
                    element.TKCheckbutton = element.Widget = tk.Checkbutton(tk_row_frame, anchor=tk.NW,
                                                                            text=element.Text, width=width,
                                                                            variable=element.TKIntVar, bd=border_depth,
                                                                            font=font,
                                                                            command=element._CheckboxHandler)
                else:
                    element.TKCheckbutton = element.Widget = tk.Checkbutton(tk_row_frame, anchor=tk.NW,
                                                                            text=element.Text, width=width,
                                                                            variable=element.TKIntVar, bd=border_depth,
                                                                            font=font)
                if element.Disabled:
                    element.TKCheckbutton.configure(state='disable')
                if element.BackgroundColor is not None and element.BackgroundColor != COLOR_SYSTEM_DEFAULT:
                    element.TKCheckbutton.configure(background=element.BackgroundColor)
                    element.TKCheckbutton.configure(selectcolor=element.BackgroundColor)
                    element.TKCheckbutton.configure(activebackground=element.BackgroundColor)
                if text_color is not None and text_color != COLOR_SYSTEM_DEFAULT:
                    element.TKCheckbutton.configure(fg=text_color)
                element.TKCheckbutton.pack(side=tk.LEFT, padx=elementpad[0], pady=elementpad[1])
                if element.Visible is False:
                    element.TKCheckbutton.pack_forget()
                if element.Tooltip is not None:
                    element.TooltipObject = ToolTip(element.TKCheckbutton, text=element.Tooltip,
                                                    timeout=DEFAULT_TOOLTIP_TIME)
            # -------------------------  PROGRESS BAR element  ------------------------- #
            elif element_type == ELEM_TYPE_PROGRESS_BAR:
                # save this form because it must be 'updated' (refreshed) solely for the purpose of updating bar
                width = element_size[0]
                fnt = tkinter.font.Font()
                char_width = fnt.measure('A')  # single character width
                progress_length = width * char_width
                progress_width = element_size[1]
                direction = element.Orientation
                if element.BarColor != (None, None):  # if element has a bar color, use it
                    bar_color = element.BarColor
                else:
                    bar_color = DEFAULT_PROGRESS_BAR_COLOR
                element.TKProgressBar = TKProgressBar(tk_row_frame, element.MaxValue, progress_length, progress_width,
                                                      orientation=direction, BarColor=bar_color,
                                                      border_width=element.BorderWidth, relief=element.Relief,
                                                      style=element.BarStyle, key=element.Key)
                element.TKProgressBar.TKProgressBarForReal.pack(side=tk.LEFT, padx=elementpad[0], pady=elementpad[1])
                if element.Visible is False:
                    element.TKProgressBar.TKProgressBarForReal.pack_forget()
                element.Widget = element.TKProgressBar.TKProgressBarForReal
                # -------------------------  RADIO BUTTON element  ------------------------- #
            elif element_type == ELEM_TYPE_INPUT_RADIO:
                element = element  # type: Radio
                width = 0 if auto_size_text else element_size[0]
                default_value = element.InitialState
                ID = element.GroupID
                # see if ID has already been placed
                value = EncodeRadioRowCol(form.ContainerElemementNumber, row_num,
                                          col_num)  # value to set intvar to if this radio is selected
                element.EncodedRadioValue = value
                if ID in toplevel_form.RadioDict:
                    RadVar = toplevel_form.RadioDict[ID]
                else:
                    RadVar = tk.IntVar()
                    toplevel_form.RadioDict[ID] = RadVar
                element.TKIntVar = RadVar  # store the RadVar in Radio object
                if default_value:  # if this radio is the one selected, set RadVar to match
                    element.TKIntVar.set(value)
                if element.ChangeSubmits:
                    element.TKRadio = element.Widget = tk.Radiobutton(tk_row_frame, anchor=tk.NW, text=element.Text,
                                                                      width=width,
                                                                      variable=element.TKIntVar, value=value,
                                                                      bd=border_depth, font=font,
                                                                      command=element._RadioHandler)
                else:
                    element.TKRadio = element.Widget = tk.Radiobutton(tk_row_frame, anchor=tk.NW, text=element.Text,
                                                                      width=width,
                                                                      variable=element.TKIntVar, value=value,
                                                                      bd=border_depth, font=font)
                if not element.BackgroundColor in (None, COLOR_SYSTEM_DEFAULT):
                    element.TKRadio.configure(background=element.BackgroundColor)
                    element.TKRadio.configure(selectcolor=element.BackgroundColor)
                if text_color is not None and text_color != COLOR_SYSTEM_DEFAULT:
                    element.TKRadio.configure(fg=text_color)
                if element.Disabled:
                    element.TKRadio['state'] = 'disabled'
                element.TKRadio.pack(side=tk.LEFT, padx=elementpad[0], pady=elementpad[1])
                if element.Visible is False:
                    element.TKRadio.pack_forget()
                if element.Tooltip is not None:
                    element.TooltipObject = ToolTip(element.TKRadio, text=element.Tooltip, timeout=DEFAULT_TOOLTIP_TIME)
                # -------------------------  SPIN element  ------------------------- #
            elif element_type == ELEM_TYPE_INPUT_SPIN:
                width, height = element_size
                width = 0 if auto_size_text else element_size[0]
                element.TKStringVar = tk.StringVar()
                element.TKSpinBox = element.Widget = tk.Spinbox(tk_row_frame, values=element.Values,
                                                                textvariable=element.TKStringVar,
                                                                width=width, bd=border_depth)
                element.TKStringVar.set(element.DefaultValue)
                element.TKSpinBox.configure(font=font)  # set wrap to width of widget
                if element.BackgroundColor is not None and element.BackgroundColor != COLOR_SYSTEM_DEFAULT:
                    element.TKSpinBox.configure(background=element.BackgroundColor)
                element.TKSpinBox.pack(side=tk.LEFT, padx=elementpad[0], pady=elementpad[1])
                if element.Visible is False:
                    element.TKSpinBox.pack_forget()
                if text_color is not None and text_color != COLOR_SYSTEM_DEFAULT:
                    element.TKSpinBox.configure(fg=text_color)
                if element.ChangeSubmits:
                    element.TKSpinBox.bind('<ButtonRelease-1>', element.SpinChangedHandler)
                if element.Disabled == True:
                    element.TKSpinBox['state'] = 'disabled'
                if element.Tooltip is not None:
                    element.TooltipObject = ToolTip(element.TKSpinBox, text=element.Tooltip,
                                                    timeout=DEFAULT_TOOLTIP_TIME)
                # -------------------------  OUTPUT element  ------------------------- #
            elif element_type == ELEM_TYPE_OUTPUT:
                width, height = element_size
                element._TKOut = element.Widget = TKOutput(tk_row_frame, width=width, height=height, bd=border_depth,
                                                           background_color=element.BackgroundColor,
                                                           text_color=text_color, font=font,
                                                           pad=elementpad)
                element._TKOut.output.configure(takefocus=0)  # make it so that Output does not get focus
                element._TKOut.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)
                if element.Visible is False:
                    element._TKOut.frame.pack_forget()
                if element.Tooltip is not None:
                    element.TooltipObject = ToolTip(element._TKOut, text=element.Tooltip, timeout=DEFAULT_TOOLTIP_TIME)
                if element.RightClickMenu or toplevel_form.RightClickMenu:
                    menu = element.RightClickMenu or toplevel_form.RightClickMenu
                    top_menu = tk.Menu(toplevel_form.TKroot, tearoff=False)
                    AddMenuItem(top_menu, menu[1], element)
                    element.TKRightClickMenu = top_menu
                    element._TKOut.bind('<Button-3>', element._RightClickMenuCallback)
                row_should_expand = True
                # -------------------------  IMAGE element  ------------------------- #
            elif element_type == ELEM_TYPE_IMAGE:
                if element.Filename is not None:
                    photo = tk.PhotoImage(file=element.Filename)
                elif element.Data is not None:
                    photo = tk.PhotoImage(data=element.Data)
                else:
                    photo = None
                    print('*ERROR laying out form.... Image Element has no image specified*')

                if photo is not None:
                    if element_size == (
                            None, None) or element_size == None or element_size == toplevel_form.DefaultElementSize:
                        width, height = photo.width(), photo.height()
                    else:
                        width, height = element_size
                    if photo is not None:
                        element.tktext_label = element.Widget = tk.Label(tk_row_frame, image=photo, width=width,
                                                                         height=height,
                                                                         bd=border_depth)
                    else:
                        element.tktext_label = element.Widget = tk.Label(tk_row_frame, width=width, height=height,
                                                                         bd=border_depth)

                    if not element.BackgroundColor in (None, COLOR_SYSTEM_DEFAULT):
                        element.tktext_label.config(background=element.BackgroundColor)

                    element.tktext_label.image = photo
                    # tktext_label.configure(anchor=tk.NW, image=photo)
                    element.tktext_label.pack(side=tk.LEFT, padx=elementpad[0], pady=elementpad[1])
                    if element.Visible is False:
                        element.tktext_label.pack_forget()
                    if element.Tooltip is not None:
                        element.TooltipObject = ToolTip(element.tktext_label, text=element.Tooltip,
                                                        timeout=DEFAULT_TOOLTIP_TIME)
                    if element.EnableEvents:
                        element.tktext_label.bind('<ButtonPress-1>', element._ClickHandler)
                    if element.RightClickMenu or toplevel_form.RightClickMenu:
                        menu = element.RightClickMenu or toplevel_form.RightClickMenu
                        top_menu = tk.Menu(toplevel_form.TKroot, tearoff=False)
                        AddMenuItem(top_menu, menu[1], element)
                        element.TKRightClickMenu = top_menu
                        element.tktext_label.bind('<Button-3>', element._RightClickMenuCallback)
                # -------------------------  Canvas element  ------------------------- #
            elif element_type == ELEM_TYPE_CANVAS:
                width, height = element_size
                if element._TKCanvas is None:
                    element._TKCanvas = element.Widget = tk.Canvas(tk_row_frame, width=width, height=height,
                                                                   bd=border_depth)
                else:
                    element._TKCanvas.master = tk_row_frame
                if element.BackgroundColor is not None and element.BackgroundColor != COLOR_SYSTEM_DEFAULT:
                    element._TKCanvas.configure(background=element.BackgroundColor, highlightthickness=0)
                element._TKCanvas.pack(side=tk.LEFT, padx=elementpad[0], pady=elementpad[1])
                if element.Visible is False:
                    element._TKCanvas.pack_forget()
                if element.Tooltip is not None:
                    element.TooltipObject = ToolTip(element._TKCanvas, text=element.Tooltip,
                                                    timeout=DEFAULT_TOOLTIP_TIME)
                if element.RightClickMenu or toplevel_form.RightClickMenu:
                    menu = element.RightClickMenu or toplevel_form.RightClickMenu
                    top_menu = tk.Menu(toplevel_form.TKroot, tearoff=False)
                    AddMenuItem(top_menu, menu[1], element)
                    element.TKRightClickMenu = top_menu
                    element._TKCanvas.bind('<Button-3>', element._RightClickMenuCallback)
                # -------------------------  Graph element  ------------------------- #
            elif element_type == ELEM_TYPE_GRAPH:
                element = element  # type: Graph
                width, height = element_size
                # I don't know why TWO canvases were being defined, on inside the other.  Was it so entire canvas can move?
                # if element._TKCanvas is None:
                #     element._TKCanvas = tk.Canvas(tk_row_frame, width=width, height=height, bd=border_depth)
                # else:
                #     element._TKCanvas.master = tk_row_frame
                element._TKCanvas2 = element.Widget = tk.Canvas(tk_row_frame, width=width, height=height,
                                                                bd=border_depth)
                element._TKCanvas2.pack(side=tk.LEFT)
                element._TKCanvas2.addtag_all('mytag')
                if element.BackgroundColor is not None and element.BackgroundColor != COLOR_SYSTEM_DEFAULT:
                    element._TKCanvas2.configure(background=element.BackgroundColor, highlightthickness=0)
                    # element._TKCanvas.configure(background=element.BackgroundColor, highlightthickness=0)
                element._TKCanvas2.pack(side=tk.LEFT, padx=elementpad[0], pady=elementpad[1])
                if element.Visible is False:
                    # element._TKCanvas.pack_forget()
                    element._TKCanvas2.pack_forget()
                if element.Tooltip is not None:
                    element.TooltipObject = ToolTip(element._TKCanvas2, text=element.Tooltip,
                                                    timeout=DEFAULT_TOOLTIP_TIME)
                if element.ChangeSubmits:
                    element._TKCanvas2.bind('<ButtonRelease-1>', element.ButtonReleaseCallBack)
                    element._TKCanvas2.bind('<ButtonPress-1>', element.ButtonPressCallBack)
                if element.DragSubmits:
                    element._TKCanvas2.bind('<Motion>', element.MotionCallBack)
                if element.RightClickMenu or toplevel_form.RightClickMenu:
                    menu = element.RightClickMenu or toplevel_form.RightClickMenu
                    top_menu = tk.Menu(toplevel_form.TKroot, tearoff=False)
                    AddMenuItem(top_menu, menu[1], element)
                    element.TKRightClickMenu = top_menu
                    element._TKCanvas2.bind('<Button-3>', element._RightClickMenuCallback)
            # -------------------------  MENUBAR element  ------------------------- #
            elif element_type == ELEM_TYPE_MENUBAR:
                element = element  # type: MenuBar
                menu_def = element.MenuDefinition
                element.TKMenu = element.Widget = tk.Menu(toplevel_form.TKroot,
                                                          tearoff=element.Tearoff)  # create the menubar
                menubar = element.TKMenu
                for menu_entry in menu_def:
                    # print(f'Adding a Menubar ENTRY {menu_entry}')
                    baritem = tk.Menu(menubar, tearoff=element.Tearoff)
                    pos = menu_entry[0].find('&')
                    # print(pos)
                    if pos != -1:
                        if pos == 0 or menu_entry[0][pos - 1] != "\\":
                            menu_entry[0] = menu_entry[0][:pos] + menu_entry[0][pos + 1:]
                    if menu_entry[0][0] == MENU_DISABLED_CHARACTER:
                        menubar.add_cascade(label=menu_entry[0][len(MENU_DISABLED_CHARACTER):], menu=baritem,
                                            underline=pos)
                        menubar.entryconfig(menu_entry[0][len(MENU_DISABLED_CHARACTER):], state='disabled')
                    else:
                        menubar.add_cascade(label=menu_entry[0], menu=baritem, underline=pos)

                    if len(menu_entry) > 1:
                        AddMenuItem(baritem, menu_entry[1], element)
                toplevel_form.TKroot.configure(menu=element.TKMenu)
            # -------------------------  Frame element  ------------------------- #
            elif element_type == ELEM_TYPE_FRAME:
                labeled_frame = element.Widget = tk.LabelFrame(tk_row_frame, text=element.Title, relief=element.Relief)
                element.TKFrame = labeled_frame
                PackFormIntoFrame(element, labeled_frame, toplevel_form)
                labeled_frame.pack(side=tk.LEFT, padx=elementpad[0], pady=elementpad[1])
                if not element.Visible:
                    labeled_frame.pack_forget()
                if element.BackgroundColor != COLOR_SYSTEM_DEFAULT and element.BackgroundColor is not None:
                    labeled_frame.configure(background=element.BackgroundColor,
                                            highlightbackground=element.BackgroundColor,
                                            highlightcolor=element.BackgroundColor)
                if element.TextColor != COLOR_SYSTEM_DEFAULT and element.TextColor is not None:
                    labeled_frame.configure(foreground=element.TextColor)
                if font is not None:
                    labeled_frame.configure(font=font)
                if element.TitleLocation is not None:
                    labeled_frame.configure(labelanchor=element.TitleLocation)
                if element.BorderWidth is not None:
                    labeled_frame.configure(borderwidth=element.BorderWidth)
                if element.Tooltip is not None:
                    element.TooltipObject = ToolTip(labeled_frame, text=element.Tooltip, timeout=DEFAULT_TOOLTIP_TIME)
                if element.RightClickMenu or toplevel_form.RightClickMenu:
                    menu = element.RightClickMenu or toplevel_form.RightClickMenu
                    top_menu = tk.Menu(toplevel_form.TKroot, tearoff=False)
                    AddMenuItem(top_menu, menu[1], element)
                    element.TKRightClickMenu = top_menu
                    labeled_frame.bind('<Button-3>', element._RightClickMenuCallback)
            # -------------------------  Tab element  ------------------------- #
            elif element_type == ELEM_TYPE_TAB:
                element.TKFrame = element.Widget = tk.Frame(form.TKNotebook)
                PackFormIntoFrame(element, element.TKFrame, toplevel_form)
                if element.Disabled:
                    form.TKNotebook.add(element.TKFrame, text=element.Title, state='disabled')
                else:
                    form.TKNotebook.add(element.TKFrame, text=element.Title)
                form.TKNotebook.pack(side=tk.LEFT, padx=elementpad[0], pady=elementpad[1])
                element.ParentNotebook = form.TKNotebook
                element.TabID = form.TabCount
                form.TabCount += 1
                if element.BackgroundColor != COLOR_SYSTEM_DEFAULT and element.BackgroundColor is not None:
                    element.TKFrame.configure(background=element.BackgroundColor,
                                              highlightbackground=element.BackgroundColor,
                                              highlightcolor=element.BackgroundColor)
                # if element.TextColor != COLOR_SYSTEM_DEFAULT and element.TextColor is not None:
                #     element.TKFrame.configure(foreground=element.TextColor)

                # ttk.Style().configure("TNotebook", background='red')
                # ttk.Style().map("TNotebook.Tab", background=[("selected", 'orange')],
                #             foreground=[("selected", 'green')])
                # ttk.Style().configure("TNotebook.Tab", background='blue', foreground='yellow')

                if element.BorderWidth is not None:
                    element.TKFrame.configure(borderwidth=element.BorderWidth)
                if element.Tooltip is not None:
                    element.TooltipObject = ToolTip(element.TKFrame, text=element.Tooltip,
                                                    timeout=DEFAULT_TOOLTIP_TIME)
                if element.RightClickMenu or toplevel_form.RightClickMenu:
                    menu = element.RightClickMenu or toplevel_form.RightClickMenu
                    top_menu = tk.Menu(toplevel_form.TKroot, tearoff=False)
                    AddMenuItem(top_menu, menu[1], element)
                    element.TKRightClickMenu = top_menu
                    element.TKFrame.bind('<Button-3>', element._RightClickMenuCallback)
            # -------------------------  TabGroup element  ------------------------- #
            elif element_type == ELEM_TYPE_TAB_GROUP:
                element=element     # type: TabGroup
                custom_style = str(element.Key) + 'customtab.TNotebook'
                style = ttk.Style(tk_row_frame)
                if element.Theme is not None:
                    style.theme_use(element.Theme)
                if element.TabLocation is not None:
                    position_dict = {'left': 'w', 'right': 'e', 'top': 'n', 'bottom': 's', 'lefttop': 'wn',
                                     'leftbottom': 'ws', 'righttop': 'en', 'rightbottom': 'es', 'bottomleft': 'sw',
                                     'bottomright': 'se', 'topleft': 'nw', 'topright': 'ne'}
                    try:
                        tab_position = position_dict[element.TabLocation]
                    except:
                        tab_position = position_dict['top']
                    style.configure(custom_style, tabposition=tab_position)

                if element.BackgroundColor is not None and element.BackgroundColor != COLOR_SYSTEM_DEFAULT:
                    style.configure(custom_style, background=element.BackgroundColor, foreground='purple')

                # style.theme_create("yummy", parent="alt", settings={
                #     "TNotebook": {"configure": {"tabmargins": [2, 5, 2, 0]}},
                #     "TNotebook.Tab": {
                #         "configure": {"padding": [5, 1], "background": mygreen},
                #         "map": {"background": [("selected", myred)],
                #                 "expand": [("selected", [1, 1, 1, 0])]}}})

                # style.configure(custom_style+'.Tab', background='red')
                if element.SelectedTitleColor != None:
                    style.map(custom_style + '.Tab', foreground=[("selected", element.SelectedTitleColor)])
                if element.TextColor is not None and element.TextColor != COLOR_SYSTEM_DEFAULT:
                    style.configure(custom_style + '.Tab', foreground=element.TextColor)
                # style.configure(custom_style, background='blue', foreground='yellow')

                element.TKNotebook = element.Widget = ttk.Notebook(tk_row_frame, style=custom_style)

                PackFormIntoFrame(element, toplevel_form.TKroot, toplevel_form)

                if element.ChangeSubmits:
                    element.TKNotebook.bind('<<NotebookTabChanged>>', element._TabGroupSelectHandler)
                if element.BorderWidth is not None:
                    element.TKNotebook.configure(borderwidth=element.BorderWidth)
                if element.Tooltip is not None:
                    element.TooltipObject = ToolTip(element.TKNotebook, text=element.Tooltip,
                                                    timeout=DEFAULT_TOOLTIP_TIME)
                # -------------------------  SLIDER element  ------------------------- #
            elif element_type == ELEM_TYPE_INPUT_SLIDER:
                slider_length = element_size[0] * CharWidthInPixels()
                slider_width = element_size[1]
                element.TKIntVar = tk.IntVar()
                element.TKIntVar.set(element.DefaultValue)
                if element.Orientation[0] == 'v':
                    range_from = element.Range[1]
                    range_to = element.Range[0]
                    slider_length += DEFAULT_MARGINS[1] * (element_size[0] * 2)  # add in the padding
                else:
                    range_from = element.Range[0]
                    range_to = element.Range[1]
                if element.ChangeSubmits:
                    tkscale = element.Widget = tk.Scale(tk_row_frame, orient=element.Orientation,
                                                        variable=element.TKIntVar,
                                                        from_=range_from, to_=range_to, resolution=element.Resolution,
                                                        length=slider_length, width=slider_width,
                                                        bd=element.BorderWidth,
                                                        relief=element.Relief, font=font,
                                                        tickinterval=element.TickInterval,
                                                        command=element._SliderChangedHandler)
                else:
                    tkscale = element.Widget = tk.Scale(tk_row_frame, orient=element.Orientation,
                                                        variable=element.TKIntVar,
                                                        from_=range_from, to_=range_to, resolution=element.Resolution,
                                                        length=slider_length, width=slider_width,
                                                        bd=element.BorderWidth,
                                                        relief=element.Relief, font=font,
                                                        tickinterval=element.TickInterval)
                tkscale.config(highlightthickness=0)
                if element.BackgroundColor is not None and element.BackgroundColor != COLOR_SYSTEM_DEFAULT:
                    tkscale.configure(background=element.BackgroundColor)
                    if DEFAULT_SCROLLBAR_COLOR != COLOR_SYSTEM_DEFAULT:
                        tkscale.config(troughcolor=DEFAULT_SCROLLBAR_COLOR)
                if element.DisableNumericDisplay:
                    tkscale.config(showvalue=0)
                if text_color is not None and text_color != COLOR_SYSTEM_DEFAULT:
                    tkscale.configure(fg=text_color)
                tkscale.pack(side=tk.LEFT, padx=elementpad[0], pady=elementpad[1])
                if element.Visible is False:
                    tkscale.pack_forget()
                element.TKScale = tkscale
                if element.Disabled == True:
                    element.TKScale['state'] = 'disabled'
                if element.Tooltip is not None:
                    element.TooltipObject = ToolTip(element.TKScale, text=element.Tooltip, timeout=DEFAULT_TOOLTIP_TIME)
            # -------------------------  TABLE element  ------------------------- #
            elif element_type == ELEM_TYPE_TABLE:
                element = element  # type: Table
                frame = tk.Frame(tk_row_frame)

                height = element.NumRows
                if element.Justification == 'left':
                    anchor = tk.W
                elif element.Justification == 'right':
                    anchor = tk.E
                else:
                    anchor = tk.CENTER
                column_widths = {}
                for row in element.Values:
                    for i, col in enumerate(row):
                        col_width = min(len(str(col)), element.MaxColumnWidth)
                        try:
                            if col_width > column_widths[i]:
                                column_widths[i] = col_width
                        except:
                            column_widths[i] = col_width
                if element.ColumnsToDisplay is None:
                    displaycolumns = element.ColumnHeadings if element.ColumnHeadings is not None else element.Values[0]
                else:
                    displaycolumns = []
                    for i, should_display in enumerate(element.ColumnsToDisplay):
                        if should_display:
                            displaycolumns.append(element.ColumnHeadings[i])
                column_headings = element.ColumnHeadings
                if element.DisplayRowNumbers:  # if display row number, tack on the numbers to front of columns
                    displaycolumns = [element.RowHeaderText, ] + displaycolumns
                    column_headings = [element.RowHeaderText, ] + element.ColumnHeadings
                element.TKTreeview = element.Widget = ttk.Treeview(frame, columns=column_headings,
                                                                   displaycolumns=displaycolumns, show='headings',
                                                                   height=height,
                                                                   selectmode=element.SelectMode, )
                treeview = element.TKTreeview
                if element.DisplayRowNumbers:
                    treeview.heading(element.RowHeaderText, text=element.RowHeaderText)  # make a dummy heading
                    treeview.column(element.RowHeaderText, width=50, anchor=anchor)

                headings = element.ColumnHeadings if element.ColumnHeadings is not None else element.Values[0]
                for i, heading in enumerate(headings):
                    treeview.heading(heading, text=heading)
                    if element.AutoSizeColumns:
                        width = max(column_widths[i], len(heading))
                    else:
                        try:
                            width = element.ColumnWidths[i]
                        except:
                            width = element.DefaultColumnWidth
                    treeview.column(heading, width=width * CharWidthInPixels(), anchor=anchor)

                # Insert values into the tree
                for i, value in enumerate(element.Values):
                    if element.DisplayRowNumbers:
                        value = [i + element.StartingRowNumber] + value
                    id = treeview.insert('', 'end', text=value, iid=i + 1, values=value, tag=i)
                if element.AlternatingRowColor is not None:  # alternating colors
                    for row in range(0, len(element.Values), 2):
                        treeview.tag_configure(row, background=element.AlternatingRowColor)
                if element.RowColors is not None:  # individual row colors
                    for row_def in element.RowColors:
                        if len(row_def) == 2:  # only background is specified
                            treeview.tag_configure(row_def[0], background=row_def[1])
                        else:
                            treeview.tag_configure(row_def[0], background=row_def[2], foreground=row_def[1])

                if element.BackgroundColor is not None and element.BackgroundColor != COLOR_SYSTEM_DEFAULT:
                    ttk.Style().configure("Treeview", background=element.BackgroundColor,
                                          fieldbackground=element.BackgroundColor)
                if element.TextColor is not None and element.TextColor != COLOR_SYSTEM_DEFAULT:
                    ttk.Style().configure("Treeview", foreground=element.TextColor)
                if element.RowHeight is not None:
                    ttk.Style().configure("Treeview", rowheight=element.RowHeight)
                ttk.Style().configure("Treeview", font=font)
                # scrollable_frame.pack(side=tk.LEFT,  padx=elementpad[0], pady=elementpad[1], expand=True, fill='both')
                treeview.bind("<<TreeviewSelect>>", element.treeview_selected)
                if element.BindReturnKey:
                    treeview.bind('<Return>', element.treeview_double_click)
                    treeview.bind('<Double-Button-1>', element.treeview_double_click)

                if not element.HideVerticalScroll:
                    scrollbar = tk.Scrollbar(frame)
                    scrollbar.pack(side=tk.RIGHT, fill='y')
                    scrollbar.config(command=treeview.yview)
                    treeview.configure(yscrollcommand=scrollbar.set)

                if not element.VerticalScrollOnly:
                    hscrollbar = tk.Scrollbar(frame, orient=tk.HORIZONTAL)
                    hscrollbar.pack(side=tk.BOTTOM, fill='x')
                    hscrollbar.config(command=treeview.xview)
                    treeview.configure(xscrollcommand=hscrollbar.set)

                element.TKTreeview.pack(side=tk.LEFT, expand=True, padx=0, pady=0, fill='both')
                if element.Visible is False:
                    element.TKTreeview.pack_forget()
                frame.pack(side=tk.LEFT, expand=True, padx=0, pady=0)
                if element.Tooltip is not None:
                    element.TooltipObject = ToolTip(element.TKTreeview, text=element.Tooltip,
                                                    timeout=DEFAULT_TOOLTIP_TIME)
                if element.RightClickMenu or toplevel_form.RightClickMenu:
                    menu = element.RightClickMenu or toplevel_form.RightClickMenu
                    top_menu = tk.Menu(toplevel_form.TKroot, tearoff=False)
                    AddMenuItem(top_menu, menu[1], element)
                    element.TKRightClickMenu = top_menu
                    element.TKTreeview.bind('<Button-3>', element._RightClickMenuCallback)
            # -------------------------  Tree element  ------------------------- #
            elif element_type == ELEM_TYPE_TREE:
                element = element  # type: Tree
                frame = tk.Frame(tk_row_frame)

                height = element.NumRows
                if element.Justification == 'left':  # justification
                    anchor = tk.W
                elif element.Justification == 'right':
                    anchor = tk.E
                else:
                    anchor = tk.CENTER

                if element.ColumnsToDisplay is None:  # Which cols to display
                    displaycolumns = element.ColumnHeadings
                else:
                    displaycolumns = []
                    for i, should_display in enumerate(element.ColumnsToDisplay):
                        if should_display:
                            displaycolumns.append(element.ColumnHeadings[i])
                column_headings = element.ColumnHeadings
                # ------------- GET THE TREEVIEW WIDGET -------------
                element.TKTreeview = element.Widget = ttk.Treeview(frame, columns=column_headings,
                                                                   displaycolumns=displaycolumns, show='tree headings',
                                                                   height=height,
                                                                   selectmode=element.SelectMode)
                treeview = element.TKTreeview
                for i, heading in enumerate(element.ColumnHeadings):  # Configure cols + headings
                    treeview.heading(heading, text=heading)
                    if element.AutoSizeColumns:
                        width = min(element.MaxColumnWidth, len(heading) + 1)
                    else:
                        try:
                            width = element.ColumnWidths[i]
                        except:
                            width = element.DefaultColumnWidth
                    treeview.column(heading, width=width * CharWidthInPixels(), anchor=anchor)

                def add_treeview_data(node):
                    """

                    :param node: 

                    """
                    # print(f'Inserting {node.key} under parent {node.parent}')
                    if node.key != '':
                        if node.icon:
                            if type(node.icon) is bytes:
                                photo = tk.PhotoImage(data=node.icon)
                            else:
                                photo = tk.PhotoImage(file=node.icon)
                            node.photo = photo
                            treeview.insert(node.parent, 'end', node.key, text=node.text, values=node.values,
                                            open=element.ShowExpanded, image=node.photo)
                        else:
                            treeview.insert(node.parent, 'end', node.key, text=node.text, values=node.values,
                                            open=element.ShowExpanded)

                    for node in node.children:
                        add_treeview_data(node)

                add_treeview_data(element.TreeData.root_node)
                treeview.column('#0', width=element.Col0Width * CharWidthInPixels(), anchor=anchor)
                # ----- configure colors -----
                if element.BackgroundColor is not None and element.BackgroundColor != COLOR_SYSTEM_DEFAULT:
                    ttk.Style().configure("Treeview", background=element.BackgroundColor,
                                          fieldbackground=element.BackgroundColor)
                if element.TextColor is not None and element.TextColor != COLOR_SYSTEM_DEFAULT:
                    ttk.Style().configure("Treeview", foreground=element.TextColor)

                ttk.Style().configure("Treeview", font=font)
                if element.RowHeight:
                    ttk.Style().configure("Treeview", rowheight=element.RowHeight)
                scrollbar = tk.Scrollbar(frame)
                scrollbar.pack(side=tk.RIGHT, fill='y')
                scrollbar.config(command=treeview.yview)
                treeview.configure(yscrollcommand=scrollbar.set)
                element.TKTreeview.pack(side=tk.LEFT, expand=True, padx=0, pady=0, fill='both')
                if element.Visible is False:
                    element.TKTreeview.pack_forget()
                frame.pack(side=tk.LEFT, expand=True, padx=0, pady=0)
                treeview.bind("<<TreeviewSelect>>", element.treeview_selected)
                if element.Tooltip is not None:  # tooltip
                    element.TooltipObject = ToolTip(element.TKTreeview, text=element.Tooltip,
                                                    timeout=DEFAULT_TOOLTIP_TIME)
                if element.RightClickMenu or toplevel_form.RightClickMenu:
                    menu = element.RightClickMenu or toplevel_form.RightClickMenu
                    top_menu = tk.Menu(toplevel_form.TKroot, tearoff=False)
                    AddMenuItem(top_menu, menu[1], element)
                    element.TKRightClickMenu = top_menu
                    element.TKTreeview.bind('<Button-3>', element._RightClickMenuCallback)
            # -------------------------  Separator element  ------------------------- #
            elif element_type == ELEM_TYPE_SEPARATOR:
                element = element  # type: VerticalSeparator
                separator = element.Widget = ttk.Separator(tk_row_frame, orient=element.Orientation, )
                separator.pack(side=tk.LEFT, padx=elementpad[0], pady=elementpad[1], fill='both', expand=True)
            # -------------------------  StatusBar element  ------------------------- #
            elif element_type == ELEM_TYPE_STATUSBAR:
                # auto_size_text = element.AutoSizeText
                display_text = element.DisplayText  # text to display
                if auto_size_text is False:
                    width, height = element_size
                else:
                    lines = display_text.split('\n')
                    max_line_len = max([len(l) for l in lines])
                    num_lines = len(lines)
                    if max_line_len > element_size[0]:  # if text exceeds element size, the will have to wrap
                        width = element_size[0]
                    else:
                        width = max_line_len
                    height = num_lines
                # ---===--- LABEL widget create and place --- #
                stringvar = tk.StringVar()
                element.TKStringVar = stringvar
                stringvar.set(display_text)
                if auto_size_text:
                    width = 0
                if element.Justification is not None:
                    justification = element.Justification
                elif toplevel_form.TextJustification is not None:
                    justification = toplevel_form.TextJustification
                else:
                    justification = DEFAULT_TEXT_JUSTIFICATION
                justify = tk.LEFT if justification == 'left' else tk.CENTER if justification == 'center' else tk.RIGHT
                anchor = tk.NW if justification == 'left' else tk.N if justification == 'center' else tk.NE
                # tktext_label = tk.Label(tk_row_frame, textvariable=stringvar, width=width, height=height,
                #                         justify=justify, bd=border_depth, font=font)
                tktext_label = element.Widget = tk.Label(tk_row_frame, textvariable=stringvar, width=width,
                                                         height=height,
                                                         justify=justify, bd=border_depth, font=font)
                # Set wrap-length for text (in PIXELS) == PAIN IN THE ASS
                wraplen = tktext_label.winfo_reqwidth() + 40  # width of widget in Pixels
                if not auto_size_text and height == 1:
                    wraplen = 0
                # print("wraplen, width, height", wraplen, width, height)
                tktext_label.configure(anchor=anchor, wraplen=wraplen)  # set wrap to width of widget
                if element.Relief is not None:
                    tktext_label.configure(relief=element.Relief)
                if element.BackgroundColor is not None and element.BackgroundColor != COLOR_SYSTEM_DEFAULT:
                    tktext_label.configure(background=element.BackgroundColor)
                if element.TextColor != COLOR_SYSTEM_DEFAULT and element.TextColor is not None:
                    tktext_label.configure(fg=element.TextColor)
                tktext_label.pack(side=tk.LEFT, padx=elementpad[0], pady=elementpad[1], fill=tk.BOTH, expand=True)
                if element.Visible is False:
                    tktext_label.pack_forget()
                element.TKText = tktext_label
                if element.ClickSubmits:
                    tktext_label.bind('<Button-1>', element._TextClickedHandler)
                if element.Tooltip is not None:
                    element.TooltipObject = ToolTip(element.TKText, text=element.Tooltip, timeout=DEFAULT_TOOLTIP_TIME)

        # ............................DONE WITH ROW pack the row of widgets ..........................#
        # done with row, pack the row of widgets
        # tk_row_frame.grid(row=row_num+2, sticky=tk.NW, padx=DEFAULT_MARGINS[0])
        tk_row_frame.pack(side=tk.TOP, anchor='nw', padx=toplevel_form.Margins[0],
                          expand=row_should_expand, fill=tk.BOTH if row_should_expand else tk.NONE)
        if form.BackgroundColor is not None and form.BackgroundColor != COLOR_SYSTEM_DEFAULT:
            tk_row_frame.configure(background=form.BackgroundColor)
        toplevel_form.TKroot.configure(padx=toplevel_form.Margins[0], pady=toplevel_form.Margins[1])
    return


def ConvertFlexToTK(MyFlexForm):
    """

    :param MyFlexForm: 

    """
    MyFlexForm  # type: Window
    master = MyFlexForm.TKroot
    master.title(MyFlexForm.Title)
    InitializeResults(MyFlexForm)
    try:
        if MyFlexForm.NoTitleBar:
            if sys.platform == 'linux':
                MyFlexForm.TKroot.wm_attributes("-type", "splash")
            else:
                MyFlexForm.TKroot.wm_overrideredirect(True)
    except:
        pass
    PackFormIntoFrame(MyFlexForm, master, MyFlexForm)
    # ....................................... DONE creating and laying out window ..........................#
    if MyFlexForm._Size != (None, None):
        master.geometry("%sx%s" % (MyFlexForm._Size[0], MyFlexForm._Size[1]))
    screen_width = master.winfo_screenwidth()  # get window info to move to middle of screen
    screen_height = master.winfo_screenheight()
    if MyFlexForm.Location != (None, None):
        x, y = MyFlexForm.Location
    elif DEFAULT_WINDOW_LOCATION != (None, None):
        x, y = DEFAULT_WINDOW_LOCATION
    else:
        master.update_idletasks()  # don't forget to do updates or values are bad
        win_width = master.winfo_width()
        win_height = master.winfo_height()
        x = screen_width / 2 - win_width / 2
        y = screen_height / 2 - win_height / 2
        if y + win_height > screen_height:
            y = screen_height - win_height
        if x + win_width > screen_width:
            x = screen_width - win_width

    move_string = '+%i+%i' % (int(x), int(y))
    master.geometry(move_string)

    master.update_idletasks()  # don't forget

    return


# ----====----====----====----====----==== STARTUP TK ====----====----====----====----====----#
def StartupTK(my_flex_form: Window):
    """

    :param my_flex_form: Window: 

    """
    # global _my_windows
    # ow = _my_windows.NumOpenWindows
    ow = Window.NumOpenWindows
    # print('Starting TK open Windows = {}'.format(ow))
    if not ow and not my_flex_form.ForceTopLevel:
        # if first window being created, make a throwaway, hidden master root.  This stops one user
        # window from becoming the child of another user window. All windows are children of this
        # hidden window
        Window.IncrementOpenCount()
        Window.hidden_master_root = tk.Tk()
        Window.hidden_master_root.attributes('-alpha', 0)  # HIDE this window really really really
        Window.hidden_master_root.wm_overrideredirect(True)
        Window.hidden_master_root.withdraw()
        root = tk.Toplevel()
    else:
        root = tk.Toplevel()

    if my_flex_form.DebuggerEnabled:
        root.bind('<Cancel>', my_flex_form._callback_main_debugger_window_create_keystroke)
        root.bind('<Pause>', my_flex_form._callback_popout_window_create_keystroke)

        # root.bind('<Cancel>', Debugger._build_main_debugger_window)
        # root.bind('<Pause>', Debugger._build_floating_window)
    try:
        root.attributes('-alpha', 0)  # hide window while building it. makes for smoother 'paint'
    except:
        pass
    if my_flex_form.BackgroundColor is not None and my_flex_form.BackgroundColor != COLOR_SYSTEM_DEFAULT:
        root.configure(background=my_flex_form.BackgroundColor)
    Window.IncrementOpenCount()

    my_flex_form.TKroot = root
    # Make moveable window
    if (my_flex_form.GrabAnywhere is not False and not (
            my_flex_form.NonBlocking and my_flex_form.GrabAnywhere is not True)):
        root.bind("<ButtonPress-1>", my_flex_form.StartMove)
        root.bind("<ButtonRelease-1>", my_flex_form.StopMove)
        root.bind("<B1-Motion>", my_flex_form.OnMotion)

    if not my_flex_form.Resizable:
        root.resizable(False, False)

    if my_flex_form.DisableMinimize:
        root.attributes("-toolwindow", 1)

    if my_flex_form.KeepOnTop:
        root.wm_attributes("-topmost", 1)

    if my_flex_form.TransparentColor is not None:
        my_flex_form.SetTransparentColor(my_flex_form.TransparentColor)

    # root.protocol("WM_DELETE_WINDOW", MyFlexForm.DestroyedCallback())
    # root.bind('<Destroy>', MyFlexForm.DestroyedCallback())
    ConvertFlexToTK(my_flex_form)

    my_flex_form.SetIcon(my_flex_form.WindowIcon)

    try:
        root.attributes('-alpha',
                        1 if my_flex_form.AlphaChannel is None else my_flex_form.AlphaChannel)  # Make window visible again
    except:
        pass

    if my_flex_form.ReturnKeyboardEvents and not my_flex_form.NonBlocking:
        root.bind("<KeyRelease>", my_flex_form._KeyboardCallback)
        root.bind("<MouseWheel>", my_flex_form._MouseWheelCallback)
    elif my_flex_form.ReturnKeyboardEvents:
        root.bind("<Key>", my_flex_form._KeyboardCallback)
        root.bind("<MouseWheel>", my_flex_form._MouseWheelCallback)

    if my_flex_form.AutoClose:
        duration = DEFAULT_AUTOCLOSE_TIME if my_flex_form.AutoCloseDuration is None else my_flex_form.AutoCloseDuration
        my_flex_form.TKAfterID = root.after(duration * 1000, my_flex_form._AutoCloseAlarmCallback)

    if my_flex_form.Timeout != None:
        my_flex_form.TKAfterID = root.after(my_flex_form.Timeout, my_flex_form._TimeoutAlarmCallback)
    if my_flex_form.NonBlocking:
        my_flex_form.TKroot.protocol("WM_DESTROY_WINDOW", my_flex_form.OnClosingCallback)
        my_flex_form.TKroot.protocol("WM_DELETE_WINDOW", my_flex_form.OnClosingCallback)
    else:  # it's a blocking form
        # print('..... CALLING MainLoop')
        my_flex_form.CurrentlyRunningMainloop = True
        my_flex_form.TKroot.protocol("WM_DESTROY_WINDOW", my_flex_form.OnClosingCallback)
        my_flex_form.TKroot.protocol("WM_DELETE_WINDOW", my_flex_form.OnClosingCallback)
        my_flex_form.TKroot.mainloop()
        my_flex_form.CurrentlyRunningMainloop = False
        my_flex_form.TimerCancelled = True
        # print('..... BACK from MainLoop')
        if not my_flex_form.FormRemainedOpen:
            Window.DecrementOpenCount()
            # _my_windows.Decrement()
        if my_flex_form.RootNeedsDestroying:
            my_flex_form.TKroot.destroy()
            my_flex_form.RootNeedsDestroying = False
    return


# ==============================_GetNumLinesNeeded ==#
# Helper function for determining how to wrap text   #
# ===================================================#
def _GetNumLinesNeeded(text, max_line_width):
    """

    :param text: 
    :param max_line_width: 

    """
    if max_line_width == 0:
        return 1
    lines = text.split('\n')
    num_lines = len(lines)  # number of original lines of text
    max_line_len = max([len(l) for l in lines])  # longest line
    lines_used = []
    for L in lines:
        lines_used.append(len(L) // max_line_width + (len(L) % max_line_width > 0))  # fancy math to round up
    total_lines_needed = sum(lines_used)
    return total_lines_needed


# ==============================  PROGRESS METER ========================================== #

def ConvertArgsToSingleString(*args):
    """

    :param *args: 

    """
    max_line_total, width_used, total_lines, = 0, 0, 0
    single_line_message = ''
    # loop through args and built a SINGLE string from them
    for message in args:
        # fancy code to check if string and convert if not is not need. Just always convert to string :-)
        # if not isinstance(message, str): message = str(message)
        message = str(message)
        longest_line_len = max([len(l) for l in message.split('\n')])
        width_used = max(longest_line_len, width_used)
        max_line_total = max(max_line_total, width_used)
        lines_needed = _GetNumLinesNeeded(message, width_used)
        total_lines += lines_needed
        single_line_message += message + '\n'
    return single_line_message, width_used, total_lines


METER_REASON_CANCELLED = 'cancelled'
METER_REASON_CLOSED = 'closed'
METER_REASON_REACHED_MAX = 'finished'
METER_OK = True
METER_STOPPED = False


class QuickMeter(object):
    """ """
    active_meters = {}
    exit_reasons = {}

    def __init__(self, title, current_value, max_value, key, *args, orientation='v', bar_color=(None, None),
                 button_color=(None, None), size=DEFAULT_PROGRESS_BAR_SIZE, border_width=None, grab_anywhere=False):
        """

        :param title: 
        :param current_value: 
        :param max_value: 
        :param key: (common_key) Used with window.FindElement and with return values
        :param *args: 
        :param orientation:  (Default value = 'v')
        :param bar_color:  (Default value = (None, None))
        :param button_color:  (Default value = (None)
        :param size: (common_key) (w,h) w=characters-wide, h=rows-high (Default value = DEFAULT_PROGRESS_BAR_SIZE)
        :param border_width:  (Default value = None)
        :param grab_anywhere: If True can grab anywhere to move the window (Default value = False)

        """
        self.start_time = datetime.datetime.utcnow()
        self.key = key
        self.orientation = orientation
        self.bar_color = bar_color
        self.size = size
        self.grab_anywhere = grab_anywhere
        self.button_color = button_color
        self.border_width = border_width
        self.title = title
        self.current_value = current_value
        self.max_value = max_value
        self.close_reason = None
        self.window = self.BuildWindow(*args)

    def BuildWindow(self, *args):
        """

        :param *args: 

        """
        layout = []
        if self.orientation.lower().startswith('h'):
            col = []
            col += [[T(''.join(map(lambda x: str(x) + '\n', args)),
                       key='_OPTMSG_')]]  ### convert all *args into one string that can be updated
            col += [[T('', size=(30, 10), key='_STATS_')],
                    [ProgressBar(max_value=self.max_value, orientation='h', key='_PROG_', size=self.size,
                                 bar_color=self.bar_color)],
                    [Cancel(button_color=self.button_color), Stretch()]]
            layout = [Column(col)]
        else:
            col = [[ProgressBar(max_value=self.max_value, orientation='v', key='_PROG_', size=self.size,
                                bar_color=self.bar_color)]]
            col2 = []
            col2 += [[T(''.join(map(lambda x: str(x) + '\n', args)),
                        key='_OPTMSG_')]]  ### convert all *args into one string that can be updated
            col2 += [[T('', size=(30, 10), key='_STATS_')],
                     [Cancel(button_color=self.button_color), Stretch()]]
            layout = [Column(col), Column(col2)]
        self.window = Window(self.title, grab_anywhere=self.grab_anywhere, border_depth=self.border_width)
        self.window.Layout([layout]).Finalize()

        return self.window

    def UpdateMeter(self, current_value, max_value, *args):  ### support for *args when updating
        """

        :param current_value: 
        :param max_value: 
        :param *args: 

        """
        self.current_value = current_value
        self.max_value = max_value
        self.window.Element('_PROG_').UpdateBar(self.current_value, self.max_value)
        self.window.Element('_STATS_').Update('\n'.join(self.ComputeProgressStats()))
        self.window.Element('_OPTMSG_').Update(
            value=''.join(map(lambda x: str(x) + '\n', args)))  ###  update the string with the args
        event, values = self.window.Read(timeout=0)
        if event in ('Cancel', None) or current_value >= max_value:
            self.window.Close()
            del (QuickMeter.active_meters[self.key])
            QuickMeter.exit_reasons[
                self.key] = METER_REASON_CANCELLED if event == 'Cancel' else METER_REASON_CLOSED if event is None else METER_REASON_REACHED_MAX
            return QuickMeter.exit_reasons[self.key]
        return METER_OK

    def ComputeProgressStats(self):
        """ """
        utc = datetime.datetime.utcnow()
        time_delta = utc - self.start_time
        total_seconds = time_delta.total_seconds()
        if not total_seconds:
            total_seconds = 1
        try:
            time_per_item = total_seconds / self.current_value
        except:
            time_per_item = 1
        seconds_remaining = (self.max_value - self.current_value) * time_per_item
        time_remaining = str(datetime.timedelta(seconds=seconds_remaining))
        time_remaining_short = (time_remaining).split(".")[0]
        time_delta_short = str(time_delta).split(".")[0]
        total_time = time_delta + datetime.timedelta(seconds=seconds_remaining)
        total_time_short = str(total_time).split(".")[0]
        self.stat_messages = [
            '{} of {}'.format(self.current_value, self.max_value),
            '{} %'.format(100 * self.current_value // self.max_value),
            '',
            ' {:6.2f} Iterations per Second'.format(self.current_value / total_seconds),
            ' {:6.2f} Seconds per Iteration'.format(total_seconds / (self.current_value if self.current_value else 1)),
            '',
            '{} Elapsed Time'.format(time_delta_short),
            '{} Time Remaining'.format(time_remaining_short),
            '{} Estimated Total Time'.format(total_time_short)]
        return self.stat_messages


def OneLineProgressMeter(title, current_value, max_value, key, *args, orientation='v', bar_color=(None, None),
                         button_color=None, size=DEFAULT_PROGRESS_BAR_SIZE, border_width=None, grab_anywhere=False):
    """

    :param title: 
    :param current_value: 
    :param max_value: 
    :param key: (common_key) Used with window.FindElement and with return values
    :param *args: 
    :param orientation:  (Default value = 'v')
    :param bar_color:  (Default value = (None, None))
    :param button_color:  (Default value = None)
    :param size: (common_key) (w,h) w=characters-wide, h=rows-high (Default value = DEFAULT_PROGRESS_BAR_SIZE)
    :param border_width:  (Default value = None)
    :param grab_anywhere: If True can grab anywhere to move the window (Default value = False)

    """
    if key not in QuickMeter.active_meters:
        meter = QuickMeter(title, current_value, max_value, key, *args, orientation=orientation, bar_color=bar_color,
                           button_color=button_color, size=size, border_width=border_width, grab_anywhere=grab_anywhere)
        QuickMeter.active_meters[key] = meter
    else:
        meter = QuickMeter.active_meters[key]

    rc = meter.UpdateMeter(current_value, max_value, *args)  ### pass the *args to to UpdateMeter function
    OneLineProgressMeter.exit_reasons = getattr(OneLineProgressMeter, 'exit_reasons', QuickMeter.exit_reasons)
    return rc == METER_OK


def OneLineProgressMeterCancel(key):
    """

    :param key: (common_key) Used with window.FindElement and with return values

    """
    try:
        meter = QuickMeter.active_meters[key]
        meter.window.Close()
        del (QuickMeter.active_meters[key])
        QuickMeter.exit_reasons[key] = METER_REASON_CANCELLED
    except:  # meter is already deleted
        return


# input is #RRGGBB
# output is #RRGGBB
def GetComplimentaryHex(color):
    """

    :param color: 

    """
    # strip the # from the beginning
    color = color[1:]
    # convert the string into hex
    color = int(color, 16)
    # invert the three bytes
    # as good as substracting each of RGB component by 255(FF)
    comp_color = 0xFFFFFF ^ color
    # convert the color back to hex by prefixing a #
    comp_color = "#%06X" % comp_color
    return comp_color


# ========================  EasyPrint           =====#
# ===================================================#
class DebugWin():
    """ """
    debug_window = None

    def __init__(self, size=(None, None), location=(None, None), font=None, no_titlebar=False, no_button=False,
                 grab_anywhere=False, keep_on_top=False, do_not_reroute_stdout=True):
        """

        :param size: (common_key) (w,h) w=characters-wide, h=rows-high (Default value = (None, None))
        :param location:  (Default value = (None)
        :param font: (common_key) specifies the font family, size, etc (Default value = None)
        :param no_titlebar:  (Default value = False)
        :param no_button:  (Default value = False)
        :param grab_anywhere: If True can grab anywhere to move the window (Default value = False)
        :param location: Location on screen to display (Default value = (None, None))
        :param do_not_reroute_stdout:  (Default value = True)

        """
        # Show a form that's a running counter
        self.size = size
        self.location = location
        self.font = font
        self.no_titlebar = no_titlebar
        self.no_button = no_button
        self.grab_anywhere = grab_anywhere
        self.keep_on_top = keep_on_top
        self.do_not_reroute_stdout = do_not_reroute_stdout

        win_size = size if size != (None, None) else DEFAULT_DEBUG_WINDOW_SIZE
        self.window = Window('Debug Window', no_titlebar=no_titlebar, auto_size_text=True, location=location,
                             font=font or ('Courier New', 10), grab_anywhere=grab_anywhere, keep_on_top=keep_on_top)
        self.output_element = Multiline(size=win_size, autoscroll=True,
                                        key='_MULTILINE_') if do_not_reroute_stdout else Output(size=win_size)

        if no_button:
            self.layout = [[self.output_element]]
        else:
            self.layout = [
                [self.output_element],
                [DummyButton('Quit'), Stretch()]
            ]
        self.window.AddRows(self.layout)
        self.window.Read(timeout=0)  # Show a non-blocking form, returns immediately
        return

    def Print(self, *args, end=None, sep=None):
        """

        :param *args: 
        :param end:  (Default value = None)
        :param sep:  (Default value = None)

        """
        sepchar = sep if sep is not None else ' '
        endchar = end if end is not None else '\n'

        if self.window is None:  # if window was destroyed alread re-open it
            self.__init__(size=self.size, location=self.location, font=self.font, no_titlebar=self.no_titlebar,
                          no_button=self.no_button, grab_anywhere=self.grab_anywhere, keep_on_top=self.keep_on_top,
                          do_not_reroute_stdout=self.do_not_reroute_stdout)
        event, values = self.window.Read(timeout=0)
        if event == 'Quit' or event is None:
            self.Close()
            self.__init__(size=self.size, location=self.location, font=self.font, no_titlebar=self.no_titlebar,
                          no_button=self.no_button, grab_anywhere=self.grab_anywhere, keep_on_top=self.keep_on_top,
                          do_not_reroute_stdout=self.do_not_reroute_stdout)
        if self.do_not_reroute_stdout:
            outstring = ''
            for arg in args:
                outstring += str(arg) + sepchar
            outstring += endchar
            self.output_element.Update(outstring, append=True)
        else:
            print(*args, sep=sepchar, end=endchar)

    def Close(self):
        """ """
        self.window.Close()
        self.window.__del__()
        self.window = None


def PrintClose():
    """ """
    EasyPrintClose()


def EasyPrint(*args, size=(None, None), end=None, sep=None, location=(None, None), font=None, no_titlebar=False,
              no_button=False, grab_anywhere=False, keep_on_top=False, do_not_reroute_stdout=True):
    """

    :param *args: 
    :param size: (common_key) (w,h) w=characters-wide, h=rows-high (Default value = (None, None))
    :param end:  (Default value = None)
    :param sep:  (Default value = None)
    :param location:  (Default value = (None)
    :param font: (common_key) specifies the font family, size, etc (Default value = None)
    :param no_titlebar:  (Default value = False)
    :param no_button:  (Default value = False)
    :param grab_anywhere: If True can grab anywhere to move the window (Default value = False)
    :param location: Location on screen to display (Default value = (None, None))
    :param do_not_reroute_stdout:  (Default value = True)

    """
    if DebugWin.debug_window is None:
        DebugWin.debug_window = DebugWin(size=size, location=location, font=font, no_titlebar=no_titlebar,
                                         no_button=no_button, grab_anywhere=grab_anywhere, keep_on_top=keep_on_top,
                                         do_not_reroute_stdout=do_not_reroute_stdout)
    DebugWin.debug_window.Print(*args, end=end, sep=sep)


Print = EasyPrint
eprint = EasyPrint


def EasyPrintClose():
    """ """
    if DebugWin.debug_window is not None:
        DebugWin.debug_window.Close()
        DebugWin.debug_window = None


# ========================  Scrolled Text Box   =====#
# ===================================================#
def PopupScrolled(*args, button_color=None, yes_no=False, auto_close=False, auto_close_duration=None, size=(None, None),
                  location=(None, None), title=None, non_blocking=False):
    """

    :param *args: 
    :param button_color:  (Default value = None)
    :param yes_no:  (Default value = False)
    :param auto_close:  (Default value = False)
    :param auto_close_duration:  (Default value = None)
    :param size: (common_key) (w,h) w=characters-wide, h=rows-high (Default value = (None, None))
    :param location:  (Default value = (None)
    :param title:  (Default value = None)
    :param non_blocking:  (Default value = False)

    """
    if not args: return
    width, height = size
    width = width if width else MESSAGE_BOX_LINE_WIDTH
    window = Window(title=title or args[0], auto_size_text=True, button_color=button_color, auto_close=auto_close,
                    auto_close_duration=auto_close_duration, location=location, resizable=True)
    max_line_total, max_line_width, total_lines, height_computed = 0, 0, 0, 0
    complete_output = ''
    for message in args:
        # fancy code to check if string and convert if not is not need. Just always convert to string :-)
        # if not isinstance(message, str): message = str(message)
        message = str(message)
        longest_line_len = max([len(l) for l in message.split('\n')])
        width_used = min(longest_line_len, width)
        max_line_total = max(max_line_total, width_used)
        max_line_width = width
        lines_needed = _GetNumLinesNeeded(message, width_used)
        height_computed += lines_needed
        complete_output += message + '\n'
        total_lines += lines_needed
    height_computed = MAX_SCROLLED_TEXT_BOX_HEIGHT if height_computed > MAX_SCROLLED_TEXT_BOX_HEIGHT else height_computed
    if height:
        height_computed = height
    window.AddRow(Multiline(complete_output, size=(max_line_width, height_computed)))
    pad = max_line_total - 15 if max_line_total > 15 else 1
    # show either an OK or Yes/No depending on paramater
    button = DummyButton if non_blocking else CloseButton
    if yes_no:
        window.AddRow(Text('', size=(pad, 1), auto_size_text=False), button('Yes'), button('No'))
    else:
        window.AddRow(Text('', size=(pad, 1), auto_size_text=False),
                      button('OK', size=(5, 1), button_color=button_color))

    if non_blocking:
        button, values = window.Read(timeout=0)
    else:
        button, values = window.Read()
        # window.Close()
    return button


ScrolledTextBox = PopupScrolled


# ============================== SetGlobalIcon ======#
# Sets the icon to be used by default                #
# ===================================================#
def SetGlobalIcon(icon):
    """

    :param icon: 

    """
    # global _my_windows

    try:
        with open(icon, 'r') as icon_file:
            pass
    except:
        raise FileNotFoundError
    # _my_windows.user_defined_icon = icon
    Window.user_defined_icon = icon
    return True


# ============================== SetOptions =========#
# Sets the icon to be used by default                #
# ===================================================#
def SetOptions(icon=None, button_color=None, element_size=(None, None), button_element_size=(None, None),
               margins=(None, None),
               element_padding=(None, None), auto_size_text=None, auto_size_buttons=None, font=None, border_width=None,
               slider_border_width=None, slider_relief=None, slider_orientation=None,
               autoclose_time=None, message_box_line_width=None,
               progress_meter_border_depth=None, progress_meter_style=None,
               progress_meter_relief=None, progress_meter_color=None, progress_meter_size=None,
               text_justification=None, background_color=None, element_background_color=None,
               text_element_background_color=None, input_elements_background_color=None, input_text_color=None,
               scrollbar_color=None, text_color=None, element_text_color=None, debug_win_size=(None, None),
               window_location=(None, None), error_button_color=(None, None), tooltip_time=None):
    """

    :param icon:  (Default value = None)
    :param button_color:  (Default value = None)
    :param element_size:  (Default value = (None, None))
    :param button_element_size:  (Default value = (None)
    :param margins:  (Default value = (None)
    :param element_padding:  (Default value = (None)
    :param auto_size_text: True if size should fit the text length (Default value = None)
    :param auto_size_buttons:  (Default value = None)
    :param font: (common_key) specifies the font family, size, etc (Default value = None)
    :param border_width:  (Default value = None)
    :param slider_border_width:  (Default value = None)
    :param slider_relief:  (Default value = None)
    :param slider_orientation:  (Default value = None)
    :param autoclose_time:  (Default value = None)
    :param message_box_line_width:  (Default value = None)
    :param progress_meter_border_depth:  (Default value = None)
    :param progress_meter_style:  (Default value = None)
    :param progress_meter_relief:  (Default value = None)
    :param progress_meter_color:  (Default value = None)
    :param progress_meter_size:  (Default value = None)
    :param text_justification:  (Default value = None)
    :param background_color: color of background (Default value = None)
    :param element_background_color:  (Default value = None)
    :param text_element_background_color:  (Default value = None)
    :param input_elements_background_color:  (Default value = None)
    :param input_text_color:  (Default value = None)
    :param scrollbar_color:  (Default value = None)
    :param text_color: color of the text (Default value = None)
    :param element_text_color:  (Default value = None)
    :param debug_win_size:  (Default value = (None)
    :param window_location:  (Default value = (None)
    :param error_button_color:  (Default value = (None)
    :param tooltip_time:  (Default value = None)

    """
    global DEFAULT_ELEMENT_SIZE
    global DEFAULT_BUTTON_ELEMENT_SIZE
    global DEFAULT_MARGINS  # Margins for each LEFT/RIGHT margin is first term
    global DEFAULT_ELEMENT_PADDING  # Padding between elements (row, col) in pixels
    global DEFAULT_AUTOSIZE_TEXT
    global DEFAULT_AUTOSIZE_BUTTONS
    global DEFAULT_FONT
    global DEFAULT_BORDER_WIDTH
    global DEFAULT_AUTOCLOSE_TIME
    global DEFAULT_BUTTON_COLOR
    global MESSAGE_BOX_LINE_WIDTH
    global DEFAULT_PROGRESS_BAR_BORDER_WIDTH
    global DEFAULT_PROGRESS_BAR_STYLE
    global DEFAULT_PROGRESS_BAR_RELIEF
    global DEFAULT_PROGRESS_BAR_COLOR
    global DEFAULT_PROGRESS_BAR_SIZE
    global DEFAULT_TEXT_JUSTIFICATION
    global DEFAULT_DEBUG_WINDOW_SIZE
    global DEFAULT_SLIDER_BORDER_WIDTH
    global DEFAULT_SLIDER_RELIEF
    global DEFAULT_SLIDER_ORIENTATION
    global DEFAULT_BACKGROUND_COLOR
    global DEFAULT_INPUT_ELEMENTS_COLOR
    global DEFAULT_ELEMENT_BACKGROUND_COLOR
    global DEFAULT_TEXT_ELEMENT_BACKGROUND_COLOR
    global DEFAULT_SCROLLBAR_COLOR
    global DEFAULT_TEXT_COLOR
    global DEFAULT_WINDOW_LOCATION
    global DEFAULT_ELEMENT_TEXT_COLOR
    global DEFAULT_INPUT_TEXT_COLOR
    global DEFAULT_TOOLTIP_TIME
    global DEFAULT_ERROR_BUTTON_COLOR
    # global _my_windows

    if icon:
        Window.user_defined_icon = icon
        # _my_windows.user_defined_icon = icon

    if button_color != None:
        DEFAULT_BUTTON_COLOR = button_color

    if element_size != (None, None):
        DEFAULT_ELEMENT_SIZE = element_size

    if button_element_size != (None, None):
        DEFAULT_BUTTON_ELEMENT_SIZE = button_element_size

    if margins != (None, None):
        DEFAULT_MARGINS = margins

    if element_padding != (None, None):
        DEFAULT_ELEMENT_PADDING = element_padding

    if auto_size_text != None:
        DEFAULT_AUTOSIZE_TEXT = auto_size_text

    if auto_size_buttons != None:
        DEFAULT_AUTOSIZE_BUTTONS = auto_size_buttons

    if font != None:
        DEFAULT_FONT = font

    if border_width != None:
        DEFAULT_BORDER_WIDTH = border_width

    if autoclose_time != None:
        DEFAULT_AUTOCLOSE_TIME = autoclose_time

    if message_box_line_width != None:
        MESSAGE_BOX_LINE_WIDTH = message_box_line_width

    if progress_meter_border_depth != None:
        DEFAULT_PROGRESS_BAR_BORDER_WIDTH = progress_meter_border_depth

    if progress_meter_style != None:
        DEFAULT_PROGRESS_BAR_STYLE = progress_meter_style

    if progress_meter_relief != None:
        DEFAULT_PROGRESS_BAR_RELIEF = progress_meter_relief

    if progress_meter_color != None:
        DEFAULT_PROGRESS_BAR_COLOR = progress_meter_color

    if progress_meter_size != None:
        DEFAULT_PROGRESS_BAR_SIZE = progress_meter_size

    if slider_border_width != None:
        DEFAULT_SLIDER_BORDER_WIDTH = slider_border_width

    if slider_orientation != None:
        DEFAULT_SLIDER_ORIENTATION = slider_orientation

    if slider_relief != None:
        DEFAULT_SLIDER_RELIEF = slider_relief

    if text_justification != None:
        DEFAULT_TEXT_JUSTIFICATION = text_justification

    if background_color != None:
        DEFAULT_BACKGROUND_COLOR = background_color

    if text_element_background_color != None:
        DEFAULT_TEXT_ELEMENT_BACKGROUND_COLOR = text_element_background_color

    if input_elements_background_color != None:
        DEFAULT_INPUT_ELEMENTS_COLOR = input_elements_background_color

    if element_background_color != None:
        DEFAULT_ELEMENT_BACKGROUND_COLOR = element_background_color

    if window_location != (None, None):
        DEFAULT_WINDOW_LOCATION = window_location

    if debug_win_size != (None, None):
        DEFAULT_DEBUG_WINDOW_SIZE = debug_win_size

    if text_color != None:
        DEFAULT_TEXT_COLOR = text_color

    if scrollbar_color != None:
        DEFAULT_SCROLLBAR_COLOR = scrollbar_color

    if element_text_color != None:
        DEFAULT_ELEMENT_TEXT_COLOR = element_text_color

    if input_text_color is not None:
        DEFAULT_INPUT_TEXT_COLOR = input_text_color

    if tooltip_time is not None:
        DEFAULT_TOOLTIP_TIME = tooltip_time

    if error_button_color != (None, None):
        DEFAULT_ERROR_BUTTON_COLOR = error_button_color

    return True


#################### ChangeLookAndFeel #######################
# Predefined settings that will change the colors and styles #
# of the elements.                                           #
##############################################################
LOOK_AND_FEEL_TABLE = {'SystemDefault':
                           {'BACKGROUND': COLOR_SYSTEM_DEFAULT,
                            'TEXT': COLOR_SYSTEM_DEFAULT,
                            'INPUT': COLOR_SYSTEM_DEFAULT, 'TEXT_INPUT': COLOR_SYSTEM_DEFAULT,
                            'SCROLL': COLOR_SYSTEM_DEFAULT,
                            'BUTTON': OFFICIAL_PYSIMPLEGUI_BUTTON_COLOR,
                            'PROGRESS': COLOR_SYSTEM_DEFAULT,
                            'BORDER': 1, 'SLIDER_DEPTH': 1,
                            'PROGRESS_DEPTH': 0},

                       'Reddit': {'BACKGROUND': '#ffffff',
                                  'TEXT': '#1a1a1b',
                                  'INPUT': '#dae0e6',
                                  'TEXT_INPUT': '#222222',
                                  'SCROLL': '#a5a4a4',
                                  'BUTTON': ('white', '#0079d3'),
                                  'PROGRESS': DEFAULT_PROGRESS_BAR_COLOR,
                                  'BORDER': 1,
                                  'SLIDER_DEPTH': 0,
                                  'PROGRESS_DEPTH': 0,
                                  'ACCENT1': '#ff5414',
                                  'ACCENT2': '#33a8ff',
                                  'ACCENT3': '#dbf0ff'},

                       'Topanga': {'BACKGROUND': '#282923',
                                   'TEXT': '#E7DB74',
                                   'INPUT': '#393a32',
                                   'TEXT_INPUT': '#E7C855',
                                   'SCROLL': '#E7C855',
                                   'BUTTON': ('#E7C855', '#284B5A'),
                                   'PROGRESS': DEFAULT_PROGRESS_BAR_COLOR,
                                   'BORDER': 1, 'SLIDER_DEPTH': 0,
                                   'PROGRESS_DEPTH': 0,
                                   'ACCENT1': '#c15226',
                                   'ACCENT2': '#7a4d5f',
                                   'ACCENT3': '#889743'},

                       'GreenTan': {'BACKGROUND': '#9FB8AD',
                                    'TEXT': COLOR_SYSTEM_DEFAULT,
                                    'INPUT': '#F7F3EC', 'TEXT_INPUT': 'black',
                                    'SCROLL': '#F7F3EC',
                                    'BUTTON': ('white', '#475841'),
                                    'PROGRESS': DEFAULT_PROGRESS_BAR_COLOR,
                                    'BORDER': 1, 'SLIDER_DEPTH': 0,
                                    'PROGRESS_DEPTH': 0},

                       'Dark': {'BACKGROUND': 'gray25',
                                'TEXT': 'white',
                                'INPUT': 'gray30',
                                'TEXT_INPUT': 'white',
                                'SCROLL': 'gray44',
                                'BUTTON': ('white', '#004F00'),
                                'PROGRESS': DEFAULT_PROGRESS_BAR_COLOR,
                                'BORDER': 1,
                                'SLIDER_DEPTH': 0,
                                'PROGRESS_DEPTH': 0},

                       'LightGreen': {'BACKGROUND': '#B7CECE',
                                      'TEXT': 'black',
                                      'INPUT': '#FDFFF7',
                                      'TEXT_INPUT': 'black',
                                      'SCROLL': '#FDFFF7',
                                      'BUTTON': ('white', '#658268'),
                                      'PROGRESS': DEFAULT_PROGRESS_BAR_COLOR,
                                      'BORDER': 1,
                                      'SLIDER_DEPTH': 0,
                                      'ACCENT1': '#76506d',
                                      'ACCENT2': '#5148f1',
                                      'ACCENT3': '#0a1c84',
                                      'PROGRESS_DEPTH': 0},

                       'Dark2': {'BACKGROUND': 'gray25',
                                 'TEXT': 'white',
                                 'INPUT': 'white',
                                 'TEXT_INPUT': 'black',
                                 'SCROLL': 'gray44',
                                 'BUTTON': ('white', '#004F00'),
                                 'PROGRESS': DEFAULT_PROGRESS_BAR_COLOR,
                                 'BORDER': 1,
                                 'SLIDER_DEPTH': 0,
                                 'PROGRESS_DEPTH': 0},

                       'Black': {'BACKGROUND': 'black',
                                 'TEXT': 'white',
                                 'INPUT': 'gray30',
                                 'TEXT_INPUT': 'white',
                                 'SCROLL': 'gray44',
                                 'BUTTON': ('black', 'white'),
                                 'PROGRESS': DEFAULT_PROGRESS_BAR_COLOR,
                                 'BORDER': 1,
                                 'SLIDER_DEPTH': 0,
                                 'PROGRESS_DEPTH': 0},

                       'Tan': {'BACKGROUND': '#fdf6e3',
                               'TEXT': '#268bd1',
                               'INPUT': '#eee8d5',
                               'TEXT_INPUT': '#6c71c3',
                               'SCROLL': '#eee8d5',
                               'BUTTON': ('white', '#063542'),
                               'PROGRESS': DEFAULT_PROGRESS_BAR_COLOR,
                               'BORDER': 1,
                               'SLIDER_DEPTH': 0,
                               'PROGRESS_DEPTH': 0},

                       'TanBlue': {'BACKGROUND': '#e5dece',
                                   'TEXT': '#063289',
                                   'INPUT': '#f9f8f4',
                                   'TEXT_INPUT': '#242834',
                                   'SCROLL': '#eee8d5',
                                   'BUTTON': ('white', '#063289'),
                                   'PROGRESS': DEFAULT_PROGRESS_BAR_COLOR,
                                   'BORDER': 1,
                                   'SLIDER_DEPTH': 0,
                                   'PROGRESS_DEPTH': 0},

                       'DarkTanBlue': {'BACKGROUND': '#242834',
                                       'TEXT': '#dfe6f8',
                                       'INPUT': '#97755c',
                                       'TEXT_INPUT': 'white',
                                       'SCROLL': '#a9afbb',
                                       'BUTTON': ('white', '#063289'),
                                       'PROGRESS': DEFAULT_PROGRESS_BAR_COLOR,
                                       'BORDER': 1,
                                       'SLIDER_DEPTH': 0,
                                       'PROGRESS_DEPTH': 0},

                       'DarkAmber': {'BACKGROUND': '#2c2825',
                                     'TEXT': '#fdcb52',
                                     'INPUT': '#705e52',
                                     'TEXT_INPUT': '#fdcb52',
                                     'SCROLL': '#705e52',
                                     'BUTTON': ('black', '#fdcb52'),
                                     'PROGRESS': DEFAULT_PROGRESS_BAR_COLOR,
                                     'BORDER': 1,
                                     'SLIDER_DEPTH': 0,
                                     'PROGRESS_DEPTH': 0},

                       'DarkBlue': {'BACKGROUND': '#1a2835',
                                    'TEXT': '#d1ecff',
                                    'INPUT': '#335267',
                                    'TEXT_INPUT': '#acc2d0',
                                    'SCROLL': '#1b6497',
                                    'BUTTON': ('black', '#fafaf8'),
                                    'PROGRESS': DEFAULT_PROGRESS_BAR_COLOR,
                                    'BORDER': 1, 'SLIDER_DEPTH': 0,
                                    'PROGRESS_DEPTH': 0},

                       'Reds': {'BACKGROUND': '#280001',
                                'TEXT': 'white',
                                'INPUT': '#d8d584',
                                'TEXT_INPUT': 'black',
                                'SCROLL': '#763e00',
                                'BUTTON': ('black', '#daad28'),
                                'PROGRESS': DEFAULT_PROGRESS_BAR_COLOR,
                                'BORDER': 1,
                                'SLIDER_DEPTH': 0,
                                'PROGRESS_DEPTH': 0},

                       'Green': {'BACKGROUND': '#82a459',
                                 'TEXT': 'black',
                                 'INPUT': '#d8d584',
                                 'TEXT_INPUT': 'black',
                                 'SCROLL': '#e3ecf3',
                                 'BUTTON': ('white', '#517239'),
                                 'PROGRESS': DEFAULT_PROGRESS_BAR_COLOR,
                                 'BORDER': 1,
                                 'SLIDER_DEPTH': 0,
                                 'PROGRESS_DEPTH': 0},

                       'BluePurple': {'BACKGROUND': '#A5CADD',
                                      'TEXT': '#6E266E',
                                      'INPUT': '#E0F5FF',
                                      'TEXT_INPUT': 'black',
                                      'SCROLL': '#E0F5FF',
                                      'BUTTON': ('white', '#303952'),
                                      'PROGRESS': DEFAULT_PROGRESS_BAR_COLOR,
                                      'BORDER': 1,
                                      'SLIDER_DEPTH': 0,
                                      'PROGRESS_DEPTH': 0},

                       'Purple': {'BACKGROUND': '#B0AAC2',
                                  'TEXT': 'black',
                                  'INPUT': '#F2EFE8',
                                  'SCROLL': '#F2EFE8',
                                  'TEXT_INPUT': 'black',
                                  'BUTTON': ('black', '#C2D4D8'),
                                  'PROGRESS': DEFAULT_PROGRESS_BAR_COLOR,
                                  'BORDER': 1,
                                  'SLIDER_DEPTH': 0,
                                  'PROGRESS_DEPTH': 0},

                       'BlueMono': {'BACKGROUND': '#AAB6D3',
                                    'TEXT': 'black',
                                    'INPUT': '#F1F4FC',
                                    'SCROLL': '#F1F4FC',
                                    'TEXT_INPUT': 'black',
                                    'BUTTON': ('white', '#7186C7'),
                                    'PROGRESS': DEFAULT_PROGRESS_BAR_COLOR,
                                    'BORDER': 1,
                                    'SLIDER_DEPTH': 0,
                                    'PROGRESS_DEPTH': 0},

                       'GreenMono': {'BACKGROUND': '#A8C1B4',
                                     'TEXT': 'black',
                                     'INPUT': '#DDE0DE',
                                     'SCROLL': '#E3E3E3',
                                     'TEXT_INPUT': 'black',
                                     'BUTTON': ('white', '#6D9F85'),
                                     'PROGRESS': DEFAULT_PROGRESS_BAR_COLOR,
                                     'BORDER': 1,
                                     'SLIDER_DEPTH': 0,
                                     'PROGRESS_DEPTH': 0},

                       'BrownBlue': {'BACKGROUND': '#64778d',
                                     'TEXT': 'white',
                                     'INPUT': '#f0f3f7',
                                     'SCROLL': '#A6B2BE',
                                     'TEXT_INPUT': 'black',
                                     'BUTTON': ('white', '#283b5b'),
                                     'PROGRESS': DEFAULT_PROGRESS_BAR_COLOR,
                                     'BORDER': 1,
                                     'SLIDER_DEPTH': 0,
                                     'PROGRESS_DEPTH': 0},

                       'BrightColors': {'BACKGROUND': '#b4ffb4',
                                        'TEXT': 'black',
                                        'INPUT': '#ffff64',
                                        'SCROLL': '#ffb482',
                                        'TEXT_INPUT': 'black',
                                        'BUTTON': ('black', '#ffa0dc'),
                                        'PROGRESS': DEFAULT_PROGRESS_BAR_COLOR,
                                        'BORDER': 1,
                                        'SLIDER_DEPTH': 0,
                                        'PROGRESS_DEPTH': 0},

                       'NeutralBlue': {'BACKGROUND': '#92aa9d',
                                       'TEXT': 'black',
                                       'INPUT': '#fcfff6',
                                       'SCROLL': '#fcfff6',
                                       'TEXT_INPUT': 'black',
                                       'BUTTON': ('black', '#d0dbbd'),
                                       'PROGRESS': DEFAULT_PROGRESS_BAR_COLOR,
                                       'BORDER': 1,
                                       'SLIDER_DEPTH': 0,
                                       'PROGRESS_DEPTH': 0},

                       'Kayak': {'BACKGROUND': '#a7ad7f',
                                 'TEXT': 'black',
                                 'INPUT': '#e6d3a8',
                                 'SCROLL': '#e6d3a8',
                                 'TEXT_INPUT': 'black',
                                 'BUTTON': ('white', '#5d907d'),
                                 'PROGRESS': DEFAULT_PROGRESS_BAR_COLOR,
                                 'BORDER': 1,
                                 'SLIDER_DEPTH': 0,
                                 'PROGRESS_DEPTH': 0},

                       'SandyBeach': {'BACKGROUND': '#efeccb',
                                      'TEXT': '#012f2f',
                                      'INPUT': '#e6d3a8',
                                      'SCROLL': '#e6d3a8',
                                      'TEXT_INPUT': '#012f2f',
                                      'BUTTON': ('white', '#046380'),
                                      'PROGRESS': DEFAULT_PROGRESS_BAR_COLOR,
                                      'BORDER': 1, 'SLIDER_DEPTH': 0,
                                      'PROGRESS_DEPTH': 0},

                       'TealMono': {'BACKGROUND': '#a8cfdd',
                                    'TEXT': 'black',
                                    'INPUT': '#dfedf2', 'SCROLL': '#dfedf2',
                                    'TEXT_INPUT': 'black',
                                    'BUTTON': ('white', '#183440'),
                                    'PROGRESS': DEFAULT_PROGRESS_BAR_COLOR,
                                    'BORDER': 1,
                                    'SLIDER_DEPTH': 0,
                                    'PROGRESS_DEPTH': 0}
                       }


def ListOfLookAndFeelValues():
    """ """
    return list(LOOK_AND_FEEL_TABLE.keys())


def ChangeLookAndFeel(index):
    """

    :param index: 

    """
    # global LOOK_AND_FEEL_TABLE

    if sys.platform == 'darwin':
        print('*** Changing look and feel is not supported on Mac platform ***')
        return

    # look and feel table

    try:
        colors = LOOK_AND_FEEL_TABLE[index]

        SetOptions(background_color=colors['BACKGROUND'],
                   text_element_background_color=colors['BACKGROUND'],
                   element_background_color=colors['BACKGROUND'],
                   text_color=colors['TEXT'],
                   input_elements_background_color=colors['INPUT'],
                   button_color=colors['BUTTON'],
                   progress_meter_color=colors['PROGRESS'],
                   border_width=colors['BORDER'],
                   slider_border_width=colors['SLIDER_DEPTH'],
                   progress_meter_border_depth=colors['PROGRESS_DEPTH'],
                   scrollbar_color=(colors['SCROLL']),
                   element_text_color=colors['TEXT'],
                   input_text_color=colors['TEXT_INPUT'])
    except:  # most likely an index out of range
        print('** Warning - Look and Feel value not valid. Change your ChangeLookAndFeel call. **')


# ============================== sprint ======#
# Is identical to the Scrolled Text Box       #
# Provides a crude 'print' mechanism but in a #
# GUI environment                             #
# ============================================#
sprint = ScrolledTextBox


# Converts an object's contents into a nice printable string.  Great for dumping debug data
def ObjToStringSingleObj(obj):
    """

    :param obj: 

    """
    if obj is None:
        return 'None'
    return str(obj.__class__) + '\n' + '\n'.join(
        (repr(item) + ' = ' + repr(obj.__dict__[item]) for item in sorted(obj.__dict__)))


def ObjToString(obj, extra='    '):
    """

    :param obj: 
    :param extra:  (Default value = '    ')

    """
    if obj is None:
        return 'None'
    return str(obj.__class__) + '\n' + '\n'.join(
        (extra + (str(item) + ' = ' +
                  (ObjToString(obj.__dict__[item], extra + '    ') if hasattr(obj.__dict__[item], '__dict__') else str(
                      obj.__dict__[item])))
         for item in sorted(obj.__dict__)))


######
#     #   ####   #####   #    #  #####    ####
#     #  #    #  #    #  #    #  #    #  #
######   #    #  #    #  #    #  #    #   ####
#        #    #  #####   #    #  #####        #
#        #    #  #       #    #  #       #    #
#         ####   #        ####   #        ####


# ------------------------------------------------------------------------------------------------------------------ #
# =====================================   Upper PySimpleGUI ======================================================== #
# ------------------------------------------------------------------------------------------------------------------ #
# ----------------------------------- The mighty Popup! ------------------------------------------------------------ #

def Popup(*args, title=None, button_color=None, background_color=None, text_color=None, button_type=POPUP_BUTTONS_OK,
          auto_close=False, auto_close_duration=None, custom_text=(None, None), non_blocking=False,
          icon=DEFAULT_WINDOW_ICON, line_width=None,
          font=None, no_titlebar=False, grab_anywhere=False, keep_on_top=False, location=(None, None)):
    """Popup - Display a popup box with as many parms as you wish to include
    :return:

    :param *args: 
    :param title:  (Default value = None)
    :param button_color:  (Default value = None)
    :param background_color: color of background (Default value = None)
    :param text_color: color of the text (Default value = None)
    :param button_type:  (Default value = POPUP_BUTTONS_OK)
    :param auto_close:  (Default value = False)
    :param auto_close_duration:  (Default value = None)
    :param custom_text:  (Default value = (None, None))
    :param non_blocking:  (Default value = False)
    :param icon: Icon to display (Default value = DEFAULT_WINDOW_ICON)
    :param line_width: Width of lines in characters (Default value = None)
    :param font: (common_key) specifies the font family, size, etc (Default value = None)
    :param no_titlebar:  (Default value = False)
    :param grab_anywhere: If True can grab anywhere to move the window (Default value = False)
    :param location: Location on screen to display (Default value = (None, None))
    :param location:  (Default value = (None)

    """
    if not args:
        args_to_print = ['']
    else:
        args_to_print = args
    if line_width != None:
        local_line_width = line_width
    else:
        local_line_width = MESSAGE_BOX_LINE_WIDTH
    _title = title if title is not None else args_to_print[0]
    window = Window(_title, auto_size_text=True, background_color=background_color, button_color=button_color,
                    auto_close=auto_close, auto_close_duration=auto_close_duration, icon=icon, font=font,
                    no_titlebar=no_titlebar, grab_anywhere=grab_anywhere, keep_on_top=keep_on_top, location=location)
    max_line_total, total_lines = 0, 0
    for message in args_to_print:
        # fancy code to check if string and convert if not is not need. Just always convert to string :-)
        # if not isinstance(message, str): message = str(message)
        message = str(message)
        if message.count('\n'):
            message_wrapped = message
        else:
            message_wrapped = textwrap.fill(message, local_line_width)
        message_wrapped_lines = message_wrapped.count('\n') + 1
        longest_line_len = max([len(l) for l in message.split('\n')])
        width_used = min(longest_line_len, local_line_width)
        max_line_total = max(max_line_total, width_used)
        # height = _GetNumLinesNeeded(message, width_used)
        height = message_wrapped_lines
        window.AddRow(
            Text(message_wrapped, auto_size_text=True, text_color=text_color, background_color=background_color))
        total_lines += height

    if non_blocking:
        PopupButton = DummyButton  # important to use or else button will close other windows too!
    else:
        PopupButton = CloseButton
    # show either an OK or Yes/No depending on paramater
    if custom_text != (None, None):
        if type(custom_text) is not tuple:
            window.AddRow(PopupButton(custom_text, size=(len(custom_text), 1), button_color=button_color, focus=True,
                                      bind_return_key=True))
        elif custom_text[1] is None:
            window.AddRow(
                PopupButton(custom_text[0], size=(len(custom_text[0]), 1), button_color=button_color, focus=True,
                            bind_return_key=True))
        else:
            window.AddRow(PopupButton(custom_text[0], button_color=button_color, focus=True, bind_return_key=True,
                                      size=(len(custom_text[0]), 1)),
                          PopupButton(custom_text[1], button_color=button_color, size=(len(custom_text[0]), 1)))
    elif button_type is POPUP_BUTTONS_YES_NO:
        window.AddRow(PopupButton('Yes', button_color=button_color, focus=True, bind_return_key=True, pad=((20, 5), 3),
                                  size=(5, 1)), PopupButton('No', button_color=button_color, size=(5, 1)))
    elif button_type is POPUP_BUTTONS_CANCELLED:
        window.AddRow(
            PopupButton('Cancelled', button_color=button_color, focus=True, bind_return_key=True, pad=((20, 0), 3)))
    elif button_type is POPUP_BUTTONS_ERROR:
        window.AddRow(PopupButton('Error', size=(6, 1), button_color=button_color, focus=True, bind_return_key=True,
                                  pad=((20, 0), 3)))
    elif button_type is POPUP_BUTTONS_OK_CANCEL:
        window.AddRow(PopupButton('OK', size=(6, 1), button_color=button_color, focus=True, bind_return_key=True),
                      PopupButton('Cancel', size=(6, 1), button_color=button_color))
    elif button_type is POPUP_BUTTONS_NO_BUTTONS:
        pass
    else:
        window.AddRow(PopupButton('OK', size=(5, 1), button_color=button_color, focus=True, bind_return_key=True,
                                  pad=((20, 0), 3)))

    if non_blocking:
        button, values = window.Read(timeout=0)
    else:
        button, values = window.Read()

    return button


# ==============================  MsgBox============#
# Lazy function. Same as calling Popup with parms   #
# This function WILL Disappear perhaps today        #
# ==================================================#
# MsgBox is the legacy call and should not be used any longer
def MsgBox(*args):
    """

    :param *args: 

    """
    raise DeprecationWarning('MsgBox is no longer supported... change your call to Popup')


# --------------------------- PopupNoButtons ---------------------------
def PopupNoButtons(*args, title=None, button_color=None, background_color=None, text_color=None, auto_close=False,
                   auto_close_duration=None, non_blocking=False, icon=DEFAULT_WINDOW_ICON, line_width=None, font=None,
                   no_titlebar=False, grab_anywhere=False, keep_on_top=False, location=(None, None)):
    """Show a Popup but without any buttons
    :return:

    :param *args: 
    :param title:  (Default value = None)
    :param button_color:  (Default value = None)
    :param background_color: color of background (Default value = None)
    :param text_color: color of the text (Default value = None)
    :param auto_close:  (Default value = False)
    :param auto_close_duration:  (Default value = None)
    :param non_blocking:  (Default value = False)
    :param icon: Icon to display (Default value = DEFAULT_WINDOW_ICON)
    :param line_width: Width of lines in characters (Default value = None)
    :param font: (common_key) specifies the font family, size, etc (Default value = None)
    :param no_titlebar:  (Default value = False)
    :param grab_anywhere: If True can grab anywhere to move the window (Default value = False)
    :param location: Location on screen to display (Default value = (None, None))
    :param location:  (Default value = (None, None))

    """
    Popup(*args, title=title, button_color=button_color, background_color=background_color, text_color=text_color,
          button_type=POPUP_BUTTONS_NO_BUTTONS,
          auto_close=auto_close, auto_close_duration=auto_close_duration, non_blocking=non_blocking, icon=icon,
          line_width=line_width,
          font=font, no_titlebar=no_titlebar, grab_anywhere=grab_anywhere, keep_on_top=keep_on_top, location=location)


# --------------------------- PopupNonBlocking ---------------------------
def PopupNonBlocking(*args, title=None, button_type=POPUP_BUTTONS_OK, button_color=None, background_color=None,
                     text_color=None,
                     auto_close=False, auto_close_duration=None, non_blocking=True, icon=DEFAULT_WINDOW_ICON,
                     line_width=None, font=None, no_titlebar=False, grab_anywhere=False, keep_on_top=False,
                     location=(None, None)):
    """Show Popup box and immediately return (does not block)
    :return:

    :param *args: 
    :param title:  (Default value = None)
    :param button_type:  (Default value = POPUP_BUTTONS_OK)
    :param button_color:  (Default value = None)
    :param background_color: color of background (Default value = None)
    :param text_color: color of the text (Default value = None)
    :param auto_close:  (Default value = False)
    :param auto_close_duration:  (Default value = None)
    :param non_blocking:  (Default value = True)
    :param icon: Icon to display (Default value = DEFAULT_WINDOW_ICON)
    :param line_width: Width of lines in characters (Default value = None)
    :param font: (common_key) specifies the font family, size, etc (Default value = None)
    :param no_titlebar:  (Default value = False)
    :param grab_anywhere: If True can grab anywhere to move the window (Default value = False)
    :param location: Location on screen to display (Default value = (None, None))
    :param location:  (Default value = (None, None))

    """
    Popup(*args, title=title, button_color=button_color, background_color=background_color, text_color=text_color,
          button_type=button_type,
          auto_close=auto_close, auto_close_duration=auto_close_duration, non_blocking=non_blocking, icon=icon,
          line_width=line_width,
          font=font, no_titlebar=no_titlebar, grab_anywhere=grab_anywhere, keep_on_top=keep_on_top, location=location)


PopupNoWait = PopupNonBlocking


# --------------------------- PopupQuick - a NonBlocking, Self-closing Popup  ---------------------------
def PopupQuick(*args, title=None, button_type=POPUP_BUTTONS_OK, button_color=None, background_color=None,
               text_color=None,
               auto_close=True, auto_close_duration=2, non_blocking=True, icon=DEFAULT_WINDOW_ICON, line_width=None,
               font=None, no_titlebar=False, grab_anywhere=False, keep_on_top=False, location=(None, None)):
    """Show Popup box that doesn't block and closes itself
    :return:

    :param *args: 
    :param title:  (Default value = None)
    :param button_type:  (Default value = POPUP_BUTTONS_OK)
    :param button_color:  (Default value = None)
    :param background_color: color of background (Default value = None)
    :param text_color: color of the text (Default value = None)
    :param auto_close:  (Default value = True)
    :param auto_close_duration:  (Default value = 2)
    :param non_blocking:  (Default value = True)
    :param icon: Icon to display (Default value = DEFAULT_WINDOW_ICON)
    :param line_width: Width of lines in characters (Default value = None)
    :param font: (common_key) specifies the font family, size, etc (Default value = None)
    :param no_titlebar:  (Default value = False)
    :param grab_anywhere: If True can grab anywhere to move the window (Default value = False)
    :param location: Location on screen to display (Default value = (None, None))
    :param location:  (Default value = (None, None))

    """
    Popup(*args, title=title, button_color=button_color, background_color=background_color, text_color=text_color,
          button_type=button_type,
          auto_close=auto_close, auto_close_duration=auto_close_duration, non_blocking=non_blocking, icon=icon,
          line_width=line_width,
          font=font, no_titlebar=no_titlebar, grab_anywhere=grab_anywhere, keep_on_top=keep_on_top, location=location)


# --------------------------- PopupQuick - a NonBlocking, Self-closing Popup with no titlebar and no buttons ---------------------------
def PopupQuickMessage(*args, title=None, button_type=POPUP_BUTTONS_NO_BUTTONS, button_color=None, background_color=None,
                      text_color=None,
                      auto_close=True, auto_close_duration=2, non_blocking=True, icon=DEFAULT_WINDOW_ICON,
                      line_width=None,
                      font=None, no_titlebar=True, grab_anywhere=False, keep_on_top=False, location=(None, None)):
    """Show Popup box that doesn't block and closes itself
    :return:

    :param *args: 
    :param title:  (Default value = None)
    :param button_type:  (Default value = POPUP_BUTTONS_NO_BUTTONS)
    :param button_color:  (Default value = None)
    :param background_color: color of background (Default value = None)
    :param text_color: color of the text (Default value = None)
    :param auto_close:  (Default value = True)
    :param auto_close_duration:  (Default value = 2)
    :param non_blocking:  (Default value = True)
    :param icon: Icon to display (Default value = DEFAULT_WINDOW_ICON)
    :param line_width: Width of lines in characters (Default value = None)
    :param font: (common_key) specifies the font family, size, etc (Default value = None)
    :param no_titlebar:  (Default value = True)
    :param grab_anywhere: If True can grab anywhere to move the window (Default value = False)
    :param location: Location on screen to display (Default value = (None, None))
    :param location:  (Default value = (None, None))

    """
    Popup(*args, title=title, button_color=button_color, background_color=background_color, text_color=text_color,
          button_type=button_type,
          auto_close=auto_close, auto_close_duration=auto_close_duration, non_blocking=non_blocking, icon=icon,
          line_width=line_width,
          font=font, no_titlebar=no_titlebar, grab_anywhere=grab_anywhere, keep_on_top=keep_on_top, location=location)


# --------------------------- PopupNoTitlebar ---------------------------
def PopupNoTitlebar(*args, title=None, button_type=POPUP_BUTTONS_OK, button_color=None, background_color=None,
                    text_color=None,
                    auto_close=False, auto_close_duration=None, non_blocking=False, icon=DEFAULT_WINDOW_ICON,
                    line_width=None, font=None, grab_anywhere=True, keep_on_top=False, location=(None, None)):
    """Display a Popup without a titlebar.   Enables grab anywhere so you can move it
    :return:

    :param *args: 
    :param title:  (Default value = None)
    :param button_type:  (Default value = POPUP_BUTTONS_OK)
    :param button_color:  (Default value = None)
    :param background_color: color of background (Default value = None)
    :param text_color: color of the text (Default value = None)
    :param auto_close:  (Default value = False)
    :param auto_close_duration:  (Default value = None)
    :param non_blocking:  (Default value = False)
    :param icon: Icon to display (Default value = DEFAULT_WINDOW_ICON)
    :param line_width: Width of lines in characters (Default value = None)
    :param font: (common_key) specifies the font family, size, etc (Default value = None)
    :param grab_anywhere:  (Default value = True)
    :param location: Location on screen to display (Default value = (None, None))
    :param location:  (Default value = (None, None))

    """
    Popup(*args, title=title, button_color=button_color, background_color=background_color, text_color=text_color,
          button_type=button_type,
          auto_close=auto_close, auto_close_duration=auto_close_duration, non_blocking=non_blocking, icon=icon,
          line_width=line_width,
          font=font, no_titlebar=True, grab_anywhere=grab_anywhere, keep_on_top=keep_on_top, location=location)


PopupNoFrame = PopupNoTitlebar
PopupNoBorder = PopupNoTitlebar
PopupAnnoying = PopupNoTitlebar


# --------------------------- PopupAutoClose ---------------------------
def PopupAutoClose(*args, title=None, button_type=POPUP_BUTTONS_OK, button_color=None, background_color=None,
                   text_color=None,
                   auto_close=True, auto_close_duration=None, non_blocking=False, icon=DEFAULT_WINDOW_ICON,
                   line_width=None, font=None, no_titlebar=False, grab_anywhere=False, keep_on_top=False,
                   location=(None, None)):
    """Popup that closes itself after some time period
    :return:

    :param *args: 
    :param title:  (Default value = None)
    :param button_type:  (Default value = POPUP_BUTTONS_OK)
    :param button_color:  (Default value = None)
    :param background_color: color of background (Default value = None)
    :param text_color: color of the text (Default value = None)
    :param auto_close:  (Default value = True)
    :param auto_close_duration:  (Default value = None)
    :param non_blocking:  (Default value = False)
    :param icon: Icon to display (Default value = DEFAULT_WINDOW_ICON)
    :param line_width: Width of lines in characters (Default value = None)
    :param font: (common_key) specifies the font family, size, etc (Default value = None)
    :param no_titlebar:  (Default value = False)
    :param grab_anywhere: If True can grab anywhere to move the window (Default value = False)
    :param location: Location on screen to display (Default value = (None, None))
    :param location:  (Default value = (None, None))

    """
    Popup(*args, title=title, button_color=button_color, background_color=background_color, text_color=text_color,
          button_type=button_type,
          auto_close=auto_close, auto_close_duration=auto_close_duration, non_blocking=non_blocking, icon=icon,
          line_width=line_width,
          font=font, no_titlebar=no_titlebar, grab_anywhere=grab_anywhere, keep_on_top=keep_on_top, location=location)


PopupTimed = PopupAutoClose


# --------------------------- PopupError ---------------------------
def PopupError(*args, title=None, button_color=(None, None), background_color=None, text_color=None, auto_close=False,
               auto_close_duration=None, non_blocking=False, icon=DEFAULT_WINDOW_ICON, line_width=None, font=None,
               no_titlebar=False, grab_anywhere=False, keep_on_top=False, location=(None, None)):
    """Popup with colored button and 'Error' as button text
    :return:

    :param *args: 
    :param title:  (Default value = None)
    :param button_color:  (Default value = (None, None))
    :param background_color: color of background (Default value = None)
    :param text_color: color of the text (Default value = None)
    :param auto_close:  (Default value = False)
    :param auto_close_duration:  (Default value = None)
    :param non_blocking:  (Default value = False)
    :param icon: Icon to display (Default value = DEFAULT_WINDOW_ICON)
    :param line_width: Width of lines in characters (Default value = None)
    :param font: (common_key) specifies the font family, size, etc (Default value = None)
    :param no_titlebar:  (Default value = False)
    :param grab_anywhere: If True can grab anywhere to move the window (Default value = False)
    :param location: Location on screen to display (Default value = (None, None))
    :param location:  (Default value = (None)

    """
    tbutton_color = DEFAULT_ERROR_BUTTON_COLOR if button_color == (None, None) else button_color
    Popup(*args, title=title, button_type=POPUP_BUTTONS_ERROR, background_color=background_color, text_color=text_color,
          non_blocking=non_blocking, icon=icon, line_width=line_width, button_color=tbutton_color,
          auto_close=auto_close,
          auto_close_duration=auto_close_duration, font=font, no_titlebar=no_titlebar, grab_anywhere=grab_anywhere,
          keep_on_top=keep_on_top, location=location)


# --------------------------- PopupCancel ---------------------------
def PopupCancel(*args, title=None, button_color=None, background_color=None, text_color=None, auto_close=False,
                auto_close_duration=None, non_blocking=False, icon=DEFAULT_WINDOW_ICON, line_width=None, font=None,
                no_titlebar=False, grab_anywhere=False, keep_on_top=False, location=(None, None)):
    """Display Popup with "cancelled" button text
    :return:

    :param *args: 
    :param title:  (Default value = None)
    :param button_color:  (Default value = None)
    :param background_color: color of background (Default value = None)
    :param text_color: color of the text (Default value = None)
    :param auto_close:  (Default value = False)
    :param auto_close_duration:  (Default value = None)
    :param non_blocking:  (Default value = False)
    :param icon: Icon to display (Default value = DEFAULT_WINDOW_ICON)
    :param line_width: Width of lines in characters (Default value = None)
    :param font: (common_key) specifies the font family, size, etc (Default value = None)
    :param no_titlebar:  (Default value = False)
    :param grab_anywhere: If True can grab anywhere to move the window (Default value = False)
    :param location: Location on screen to display (Default value = (None, None))
    :param location:  (Default value = (None, None))

    """
    Popup(*args, title=title, button_type=POPUP_BUTTONS_CANCELLED, background_color=background_color,
          text_color=text_color,
          non_blocking=non_blocking, icon=icon, line_width=line_width, button_color=button_color, auto_close=auto_close,
          auto_close_duration=auto_close_duration, font=font, no_titlebar=no_titlebar, grab_anywhere=grab_anywhere,
          keep_on_top=keep_on_top, location=location)


# --------------------------- PopupOK ---------------------------
def PopupOK(*args, title=None, button_color=None, background_color=None, text_color=None, auto_close=False,
            auto_close_duration=None, non_blocking=False, icon=DEFAULT_WINDOW_ICON, line_width=None, font=None,
            no_titlebar=False, grab_anywhere=False, keep_on_top=False, location=(None, None)):
    """Display Popup with OK button only
    :return:

    :param *args: 
    :param title:  (Default value = None)
    :param button_color:  (Default value = None)
    :param background_color: color of background (Default value = None)
    :param text_color: color of the text (Default value = None)
    :param auto_close:  (Default value = False)
    :param auto_close_duration:  (Default value = None)
    :param non_blocking:  (Default value = False)
    :param icon: Icon to display (Default value = DEFAULT_WINDOW_ICON)
    :param line_width: Width of lines in characters (Default value = None)
    :param font: (common_key) specifies the font family, size, etc (Default value = None)
    :param no_titlebar:  (Default value = False)
    :param grab_anywhere: If True can grab anywhere to move the window (Default value = False)
    :param location: Location on screen to display (Default value = (None, None))
    :param location:  (Default value = (None, None))

    """
    Popup(*args, title=title, button_type=POPUP_BUTTONS_OK, background_color=background_color, text_color=text_color,
          non_blocking=non_blocking, icon=icon, line_width=line_width, button_color=button_color, auto_close=auto_close,
          auto_close_duration=auto_close_duration, font=font, no_titlebar=no_titlebar, grab_anywhere=grab_anywhere,
          keep_on_top=keep_on_top, location=location)


# --------------------------- PopupOKCancel ---------------------------
def PopupOKCancel(*args, title=None, button_color=None, background_color=None, text_color=None, auto_close=False,
                  auto_close_duration=None, non_blocking=False, icon=DEFAULT_WINDOW_ICON, line_width=None, font=None,
                  no_titlebar=False, grab_anywhere=False, keep_on_top=False, location=(None, None)):
    """Display popup with OK and Cancel buttons
    :return: OK, Cancel or None

    :param *args: 
    :param title:  (Default value = None)
    :param button_color:  (Default value = None)
    :param background_color: color of background (Default value = None)
    :param text_color: color of the text (Default value = None)
    :param auto_close:  (Default value = False)
    :param auto_close_duration:  (Default value = None)
    :param non_blocking:  (Default value = False)
    :param icon: Icon to display (Default value = DEFAULT_WINDOW_ICON)
    :param line_width: Width of lines in characters (Default value = None)
    :param font: (common_key) specifies the font family, size, etc (Default value = None)
    :param no_titlebar:  (Default value = False)
    :param grab_anywhere: If True can grab anywhere to move the window (Default value = False)
    :param location: Location on screen to display (Default value = (None, None))
    :param location:  (Default value = (None, None))

    """
    return Popup(*args, title=title, button_type=POPUP_BUTTONS_OK_CANCEL, background_color=background_color,
                 text_color=text_color,
                 non_blocking=non_blocking, icon=icon, line_width=line_width, button_color=button_color,
                 auto_close=auto_close, auto_close_duration=auto_close_duration, font=font, no_titlebar=no_titlebar,
                 grab_anywhere=grab_anywhere, keep_on_top=keep_on_top, location=location)


# --------------------------- PopupYesNo ---------------------------
def PopupYesNo(*args, title=None, button_color=None, background_color=None, text_color=None, auto_close=False,
               auto_close_duration=None, non_blocking=False, icon=DEFAULT_WINDOW_ICON, line_width=None, font=None,
               no_titlebar=False, grab_anywhere=False, keep_on_top=False, location=(None, None)):
    """Display Popup with Yes and No buttons
    :return: Yes, No or None

    :param *args: 
    :param title:  (Default value = None)
    :param button_color:  (Default value = None)
    :param background_color: color of background (Default value = None)
    :param text_color: color of the text (Default value = None)
    :param auto_close:  (Default value = False)
    :param auto_close_duration:  (Default value = None)
    :param non_blocking:  (Default value = False)
    :param icon: Icon to display (Default value = DEFAULT_WINDOW_ICON)
    :param line_width: Width of lines in characters (Default value = None)
    :param font: (common_key) specifies the font family, size, etc (Default value = None)
    :param no_titlebar:  (Default value = False)
    :param grab_anywhere: If True can grab anywhere to move the window (Default value = False)
    :param location: Location on screen to display (Default value = (None, None))
    :param location:  (Default value = (None, None))

    """
    return Popup(*args, title=title, button_type=POPUP_BUTTONS_YES_NO, background_color=background_color,
                 text_color=text_color,
                 non_blocking=non_blocking, icon=icon, line_width=line_width, button_color=button_color,
                 auto_close=auto_close, auto_close_duration=auto_close_duration, font=font, no_titlebar=no_titlebar,
                 grab_anywhere=grab_anywhere, keep_on_top=keep_on_top, location=location)


##############################################################################
#   The PopupGet_____ functions - Will return user input                     #
##############################################################################

# --------------------------- PopupGetFolder ---------------------------


def PopupGetFolder(message, title=None, default_path='', no_window=False, size=(None, None), button_color=None,
                   background_color=None, text_color=None, icon=DEFAULT_WINDOW_ICON, font=None, no_titlebar=False,
                   grab_anywhere=False, keep_on_top=False, location=(None, None), initial_folder=None):
    """Display popup with text entry field and browse button. Browse for folder
    :return: Contents of text field. None if closed using X or cancelled

    :param message: 
    :param title:  (Default value = None)
    :param default_path:  (Default value = '')
    :param no_window:  (Default value = False)
    :param size: (common_key) (w,h) w=characters-wide, h=rows-high (Default value = (None, None))
    :param button_color:  (Default value = None)
    :param background_color: color of background (Default value = None)
    :param text_color: color of the text (Default value = None)
    :param icon: Icon to display (Default value = DEFAULT_WINDOW_ICON)
    :param font: (common_key) specifies the font family, size, etc (Default value = None)
    :param no_titlebar:  (Default value = False)
    :param grab_anywhere: If True can grab anywhere to move the window (Default value = False)
    :param location: Location on screen to display (Default value = (None, None))
    :param location:  (Default value = (None)
    :param initial_folder:  (Default value = None)

    """

    # global _my_windows
    if no_window:
        if not Window.hidden_master_root:
            # if first window being created, make a throwaway, hidden master root.  This stops one user
            # window from becoming the child of another user window. All windows are children of this
            # hidden window
            Window.IncrementOpenCount()
            Window.hidden_master_root = tk.Tk()
            Window.hidden_master_root.attributes('-alpha', 0)  # HIDE this window really really really
            Window.hidden_master_root.wm_overrideredirect(True)
            Window.hidden_master_root.withdraw()
        root = tk.Toplevel()

        try:
            root.attributes('-alpha', 0)  # hide window while building it. makes for smoother 'paint'
            root.wm_overrideredirect(True)
            root.withdraw()
        except:
            pass
        folder_name = tk.filedialog.askdirectory()  # show the 'get folder' dialog box

        root.destroy()
        if Window.NumOpenWindows == 1:
            Window.NumOpenWindows = 0
            Window.hidden_master_root.destroy()
            Window.hidden_master_root = None

        return folder_name

    layout = [[Text(message, auto_size_text=True, text_color=text_color, background_color=background_color)],
              [InputText(default_text=default_path, size=size, key='_INPUT_'),
               FolderBrowse(initial_folder=initial_folder)],
              [CloseButton('Ok', size=(5, 1), bind_return_key=True), CloseButton('Cancel', size=(5, 1))]]

    window = Window(title=title or message, layout=layout, icon=icon, auto_size_text=True, button_color=button_color,
                    background_color=background_color,
                    font=font, no_titlebar=no_titlebar, grab_anywhere=grab_anywhere, keep_on_top=keep_on_top,
                    location=location)

    button, values = window.Read()
    window.Close()
    if button != 'Ok':
        return None
    else:
        return values['_INPUT_']


# --------------------------- PopupGetFile ---------------------------

def PopupGetFile(message, title=None, default_path='', default_extension='', save_as=False, multiple_files=False,
                 file_types=(("ALL Files", "*.*"),),
                 no_window=False, size=(None, None), button_color=None, background_color=None, text_color=None,
                 icon=DEFAULT_WINDOW_ICON, font=None, no_titlebar=False, grab_anywhere=False, keep_on_top=False,
                 location=(None, None), initial_folder=None):
    """Display popup with text entry field and browse button. Browse for file
    :return:  string representing the path chosen, None if cancelled or window closed with X

    :param message: 
    :param title:  (Default value = None)
    :param default_path:  (Default value = '')
    :param default_extension:  (Default value = '')
    :param save_as:  (Default value = False)
    :param multiple_files:  (Default value = False)
    :param file_types:  (Default value = (("ALL Files", "*.*")))
    :param no_window:  (Default value = False)
    :param size: (common_key) (w,h) w=characters-wide, h=rows-high (Default value = (None, None))
    :param button_color:  (Default value = None)
    :param background_color: color of background (Default value = None)
    :param text_color: color of the text (Default value = None)
    :param icon: Icon to display (Default value = DEFAULT_WINDOW_ICON)
    :param font: (common_key) specifies the font family, size, etc (Default value = None)
    :param no_titlebar:  (Default value = False)
    :param grab_anywhere: If True can grab anywhere to move the window (Default value = False)
    :param location: Location on screen to display (Default value = (None, None))
    :param location:  (Default value = (None)
    :param initial_folder:  (Default value = None)

    """

    if no_window:
        if not Window.hidden_master_root:
            # if first window being created, make a throwaway, hidden master root.  This stops one user
            # window from becoming the child of another user window. All windows are children of this
            # hidden window
            Window.IncrementOpenCount()
            Window.hidden_master_root = tk.Tk()
            Window.hidden_master_root.attributes('-alpha', 0)  # HIDE this window really really really
            Window.hidden_master_root.wm_overrideredirect(True)
            Window.hidden_master_root.withdraw()
        root = tk.Toplevel()

        try:
            root.attributes('-alpha', 0)  # hide window while building it. makes for smoother 'paint'
            root.wm_overrideredirect(True)
            root.withdraw()
        except:
            pass
        if save_as:
            filename = tk.filedialog.asksaveasfilename(filetypes=file_types,
                                                       defaultextension=default_extension)  # show the 'get file' dialog box
        elif multiple_files:
            filename = tk.filedialog.askopenfilenames(filetypes=file_types,
                                                      defaultextension=default_extension)  # show the 'get file' dialog box
        else:
            filename = tk.filedialog.askopenfilename(filetypes=file_types,
                                                     defaultextension=default_extension)  # show the 'get files' dialog box

        root.destroy()
        if Window.NumOpenWindows == 1:
            Window.NumOpenWindows = 0
            Window.hidden_master_root.destroy()
            Window.hidden_master_root = None
        if not multiple_files and type(filename) in (tuple, list):
            filename = filename[0]
        return filename

    if save_as:
        browse_button = SaveAs(file_types=file_types, initial_folder=initial_folder)
    elif multiple_files:
        browse_button = FilesBrowse(file_types=file_types, initial_folder=initial_folder)
    else:
        browse_button = FileBrowse(file_types=file_types, initial_folder=initial_folder)

    layout = [[Text(message, auto_size_text=True, text_color=text_color, background_color=background_color)],
              [InputText(default_text=default_path, size=size, key='_INPUT_'), browse_button],
              [CloseButton('Ok', size=(6, 1), bind_return_key=True), CloseButton('Cancel', size=(6, 1))]]

    window = Window(title=title or message, layout=layout, icon=icon, auto_size_text=True, button_color=button_color,
                    font=font,
                    background_color=background_color,
                    no_titlebar=no_titlebar, grab_anywhere=grab_anywhere, keep_on_top=keep_on_top, location=location)

    button, values = window.Read()
    window.Close()
    if button != 'Ok':
        return None
    else:
        path = values['_INPUT_']
        return path


# --------------------------- PopupGetText ---------------------------

def PopupGetText(message, title=None, default_text='', password_char='', size=(None, None), button_color=None,
                 background_color=None, text_color=None, icon=DEFAULT_WINDOW_ICON, font=None, no_titlebar=False,
                 grab_anywhere=False, keep_on_top=False, location=(None, None)):
    """Display Popup with text entry field
    :return: Text entered or None if window was closed

    :param message: 
    :param title:  (Default value = None)
    :param default_text:  (Default value = '')
    :param password_char: Passwork character if this is a password field (Default value = '')
    :param size: (common_key) (w,h) w=characters-wide, h=rows-high (Default value = (None, None))
    :param button_color:  (Default value = None)
    :param background_color: color of background (Default value = None)
    :param text_color: color of the text (Default value = None)
    :param icon: Icon to display (Default value = DEFAULT_WINDOW_ICON)
    :param font: (common_key) specifies the font family, size, etc (Default value = None)
    :param no_titlebar:  (Default value = False)
    :param grab_anywhere: If True can grab anywhere to move the window (Default value = False)
    :param location: Location on screen to display (Default value = (None, None))
    :param location:  (Default value = (None)

    """

    layout = [[Text(message, auto_size_text=True, text_color=text_color, background_color=background_color, font=font)],
              [InputText(default_text=default_text, size=size, key='_INPUT_', password_char=password_char)],
              [CloseButton('Ok', size=(5, 1), bind_return_key=True), CloseButton('Cancel', size=(5, 1))]]

    window = Window(title=title or message, layout=layout, icon=icon, auto_size_text=True, button_color=button_color,
                    no_titlebar=no_titlebar,
                    background_color=background_color, grab_anywhere=grab_anywhere, keep_on_top=keep_on_top,
                    location=location)

    button, values = window.Read()
    window.Close()
    if button != 'Ok':
        return None
    else:
        path = values['_INPUT_']
        return path


def PopupAnimated(image_source, message=None, background_color=None, text_color=None, font=None, no_titlebar=True,
                  grab_anywhere=True, keep_on_top=True, location=(None, None), alpha_channel=None,
                  time_between_frames=0, transparent_color=None):
    """

    :param image_source: 
    :param message:  (Default value = None)
    :param background_color: color of background (Default value = None)
    :param text_color: color of the text (Default value = None)
    :param font: (common_key) specifies the font family, size, etc (Default value = None)
    :param no_titlebar:  (Default value = True)
    :param grab_anywhere:  (Default value = True)
    :param keep_on_top:  (Default value = True)
    :param location:  (Default value = (None, None))
    :param alpha_channel:  (Default value = None)
    :param time_between_frames:  (Default value = 0)
    :param transparent_color:  (Default value = None)

    """
    if image_source is None:
        for image in Window.animated_popup_dict:
            window = Window.animated_popup_dict[image]
            window.Close()
        Window.animated_popup_dict = {}
        return

    if image_source not in Window.animated_popup_dict:
        if type(image_source) is bytes or len(image_source) > 300:
            layout = [[Image(data=image_source, background_color=background_color, key='_IMAGE_', )], ]
        else:
            layout = [[Image(filename=image_source, background_color=background_color, key='_IMAGE_', )], ]
        if message:
            layout.append([Text(message, background_color=background_color, text_color=text_color, font=font)])

        window = Window('Animated GIF', layout, no_titlebar=no_titlebar, grab_anywhere=grab_anywhere,
                        keep_on_top=keep_on_top, background_color=background_color, location=location,
                        alpha_channel=alpha_channel, element_padding=(0, 0), margins=(0, 0),
                        transparent_color=transparent_color).Finalize()
        Window.animated_popup_dict[image_source] = window
    else:
        window = Window.animated_popup_dict[image_source]
        window.Element('_IMAGE_').UpdateAnimation(image_source, time_between_frames=time_between_frames)

    window.Refresh()  # call refresh instead of Read to save significant CPU time


#####################################################################################################
# Debugger
#####################################################################################################


PSGDebugLogo = b'R0lGODlhMgAtAPcAAAAAADD/2akK/4yz0pSxyZWyy5u3zZ24zpW30pG52J250J+60aC60KS90aDC3a3E163F2K3F2bPI2bvO3rzP3qvJ4LHN4rnR5P/zuf/zuv/0vP/0vsDS38XZ6cnb6f/xw//zwv/yxf/1w//zyP/1yf/2zP/3z//30wAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACH5BAEAAP8ALAAAAAAyAC0AAAj/AP8JHEiwoMGDCBMqXMiwoUOFAiJGXBigYoAPDxlK3CigwUGLIAOEyIiQI8cCBUOqJFnQpEkGA1XKZPlPgkuXBATK3JmRws2bB3TuXNmQw8+jQoeCbHj0qIGkSgNobNoUqlKIVJs++BfV4oiEWalaHVpyosCwJidw7Sr1YMQFBDn+y4qSbUW3AiDElXiWqoK1bPEKGLixr1jAXQ9GuGn4sN22Bl02roo4Kla+c8OOJbsQM9rNPJlORlr5asbPpTk/RP2YJGu7rjWnDm2RIQLZrSt3zgp6ZmqwmkHAng3ccWDEMe8Kpnw8JEHlkXnPdh6SxHPILaU/dp60LFUP07dfRq5aYntohAO0m+c+nvT6pVMPZ3jv8AJu8xktyNbw+ATJDtKFBx9NlA20gWU0DVQBYwZhsJMICRrkwEYJJGRCSBtEqGGCAQEAOw=='

red_x = b"R0lGODlhEAAQAPeQAIsAAI0AAI4AAI8AAJIAAJUAAJQCApkAAJoAAJ4AAJkJCaAAAKYAAKcAAKcCAKcDA6cGAKgAAKsAAKsCAKwAAK0AAK8AAK4CAK8DAqUJAKULAKwLALAAALEAALIAALMAALMDALQAALUAALYAALcEALoAALsAALsCALwAAL8AALkJAL4NAL8NAKoTAKwbAbEQALMVAL0QAL0RAKsREaodHbkQELMsALg2ALk3ALs+ALE2FbgpKbA1Nbc1Nb44N8AAAMIWAMsvAMUgDMcxAKVABb9NBbVJErFYEq1iMrtoMr5kP8BKAMFLAMxKANBBANFCANJFANFEB9JKAMFcANFZANZcANpfAMJUEMZVEc5hAM5pAMluBdRsANR8AM9YOrdERMpIQs1UVMR5WNt8X8VgYMdlZcxtYtx4YNF/btp9eraNf9qXXNCCZsyLeNSLd8SSecySf82kd9qqc9uBgdyBgd+EhN6JgtSIiNuJieGHhOGLg+GKhOKamty1ste4sNO+ueenp+inp+HHrebGrefKuOPTzejWzera1O7b1vLb2/bl4vTu7fbw7ffx7vnz8f///wAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACH5BAEAAJAALAAAAAAQABAAAAjUACEJHEiwYEEABniQKfNFgQCDkATQwAMokEU+PQgUFDAjjR09e/LUmUNnh8aBCcCgUeRmzBkzie6EeQBAoAAMXuA8ciRGCaJHfXzUMCAQgYooWN48anTokR8dQk4sELggBhQrU9Q8evSHiJQgLCIIfMDCSZUjhbYuQkLFCRAMAiOQGGLE0CNBcZYmaRIDLqQFGF60eTRoSxc5jwjhACFWIAgMLtgUocJFy5orL0IQRHAiQgsbRZYswbEhBIiCCH6EiJAhAwQMKU5DjHCi9gnZEHMTDAgAOw=="

COLOR_SCHEME = 'LightGreen'

WIDTH_VARIABLES = 23
WIDTH_RESULTS = 46

WIDTH_WATCHER_VARIABLES = 20
WIDTH_WATCHER_RESULTS = 60

WIDTH_LOCALS = 80
NUM_AUTO_WATCH = 9

MAX_LINES_PER_RESULT_FLOATING = 4
MAX_LINES_PER_RESULT_MAIN      = 3

POPOUT_WINDOW_FONT = 'Sans 8'

class Debugger():
    """ """

    debugger = None

    #     #                    ######
    ##   ##   ##   # #    #    #     # ###### #####  #    #  ####   ####  ###### #####
    # # # #  #  #  # ##   #    #     # #      #    # #    # #    # #    # #      #    #
    #  #  # #    # # # #  #    #     # #####  #####  #    # #      #      #####  #    #
    #     # ###### # #  # #    #     # #      #    # #    # #  ### #  ### #      #####
    #     # #    # # #   ##    #     # #      #    # #    # #    # #    # #      #   #
    #     # #    # # #    #    ######  ###### #####   ####   ####   ####  ###### #    #

    def __init__(self):
        """ """
        self.watcher_window = None  # type: Window
        self.popout_window = None   # type: Window
        self.local_choices = {}
        self.myrc = ''
        self.custom_watch = ''
        self.locals = {}
        self.globals = {}
        self.popout_choices = {}



    def _build_main_debugger_window_callback(self, events):
        """

        :param events: 

        """
        self._build_main_debugger_window()

    # Includes the DUAL PANE (now 2 tabs)!  Don't forget REPL is there too!
    def _build_main_debugger_window(self, location=(None, None)):
        """

        :param location:  (Default value = (None, None))

        """
        ChangeLookAndFeel(COLOR_SCHEME)

        def InVar(key1):
            """

            :param key1: 

            """
            row1 = [T('    '),
                    I(key=key1, size=(WIDTH_VARIABLES, 1)),
                    T('', key=key1 + 'CHANGED_', size=(WIDTH_RESULTS, 1)), B('Detail', key=key1 + 'DETAIL_'),
                    B('Obj', key=key1 + 'OBJ_'), ]
            return row1

        variables_frame = [InVar('_VAR0_'),
                           InVar('_VAR1_'),
                           InVar('_VAR2_'), ]

        interactive_frame = [[T('>>> '), In(size=(83, 1), key='_REPL_',
                                tooltip='Type in any "expression" or "statement"\n and it will be disaplayed below.\nPress RETURN KEY instead of "Go"\nbutton for faster use'),
                              B('Go', bind_return_key=True, visible=True)],
                             [Multiline(size=(93, 26), key='_OUTPUT_', autoscroll=True, do_not_clear=True)], ]

        autowatch_frame = [[Button('Choose Variables To Auto Watch', key='_LOCALS_'),
                            Button('Clear All Auto Watches'),
                            Button('Show All Variables', key='_SHOW_ALL_'),
                            Button('Locals', key='_ALL_LOCALS_'),
                            Button('Globals', key='_GLOBALS_'),
                            Button('Popout', key='_POPOUT_')]]

        var_layout = []
        for i in range(NUM_AUTO_WATCH):
            var_layout.append([T('', size=(WIDTH_WATCHER_VARIABLES, 1), key='_WATCH%s_' % i),
              T('', size=(WIDTH_WATCHER_RESULTS, MAX_LINES_PER_RESULT_MAIN), key='_WATCH%s_RESULT_' % i,
                    )])

        col1 = [
            # [Frame('Auto Watches', autowatch_frame+variable_values, title_color='blue')]
            [Frame('Auto Watches', autowatch_frame+var_layout, title_color='blue')]
        ]

        col2 = [
            [Frame('Variables or Expressions to Watch', variables_frame, title_color='blue'), ],
            [Frame('REPL-Light - Press Enter To Execute Commands', interactive_frame, title_color='blue'), ]
        ]

        # Tab based layout
        layout = [[TabGroup([[Tab('Variables', col1), Tab('REPL & Watches', col2)]])],
                  [Button('', image_data=red_x, key='_EXIT_', button_color=None),]]

        # ------------------------------- Create main window -------------------------------
        window = Window("PySimpleGUI Debugger", layout, icon=PSGDebugLogo, margins=(0, 0), location=location).Finalize()
        window.Element('_VAR1_').SetFocus()
        self.watcher_window = window
        ChangeLookAndFeel('SystemDefault')           # set look and feel to default before exiting
        return window

    #     #                    #######                               #
    ##   ##   ##   # #    #    #       #    # ###### #    # #####    #        ####   ####  #####
    # # # #  #  #  # ##   #    #       #    # #      ##   #   #      #       #    # #    # #    #
    #  #  # #    # # # #  #    #####   #    # #####  # #  #   #      #       #    # #    # #    #
    #     # ###### # #  # #    #       #    # #      #  # #   #      #       #    # #    # #####
    #     # #    # # #   ##    #        #  #  #      #   ##   #      #       #    # #    # #
    #     # #    # # #    #    #######   ##   ###### #    #   #      #######  ####   ####  #

    def _refresh_main_debugger_window(self, mylocals, myglobals):
        """

        :param mylocals: 
        :param myglobals: 

        """
        if not self.watcher_window:     # if there is no window setup, nothing to do
            return False
        event, values = self.watcher_window.Read(timeout=1)
        if event in (None, 'Exit', '_EXIT_'):  # EXIT BUTTON / X BUTTON
            try:
                self.watcher_window.Close()
            except: pass
            self.watcher_window = None
            return False
        # ------------------------------- Process events from REPL Tab -------------------------------
        cmd = values['_REPL_']                  # get the REPL entered
        # BUTTON - GO (NOTE - This button is invisible!!)
        if event == 'Go':  # GO BUTTON
            self.watcher_window.Element('_REPL_').Update('')
            self.watcher_window.Element('_OUTPUT_').Update(">>> {}\n".format(cmd), append=True, autoscroll=True)

            try:
                result = eval('{}'.format(cmd), myglobals, mylocals)
            except Exception as e:
                try:
                    result = exec('{}'.format(cmd), myglobals, mylocals)
                except Exception as e:
                    result = 'Exception {}\n'.format(e)

            self.watcher_window.Element('_OUTPUT_').Update('{}\n'.format(result), append=True, autoscroll=True)
        # BUTTON - DETAIL
        elif event.endswith('_DETAIL_'):  # DETAIL BUTTON
            var = values['_VAR{}_'.format(event[4])]
            try:
                result = str(eval(str(var), myglobals, mylocals))
            except:
                result = ''
            PopupScrolled(str(values['_VAR{}_'.format(event[4])]) + '\n' + result, title=var, non_blocking=True)
        # BUTTON - OBJ
        elif event.endswith('_OBJ_'):  # OBJECT BUTTON
            var = values['_VAR{}_'.format(event[4])]
            try:
                result = ObjToStringSingleObj(mylocals[var])
            except Exception as e:
                result = '{}\nError showing object {}'.format(e, var)
            PopupScrolled(str(var) + '\n' + str(result), title=var, non_blocking=True)
        # ------------------------------- Process Watch Tab -------------------------------
        # BUTTON - Choose Locals to see
        elif event == '_LOCALS_':  # Show all locals BUTTON
            self._choose_auto_watches(mylocals)
        # BUTTON - Locals (quick popup)
        elif event == '_ALL_LOCALS_':
            self._display_all_vars(mylocals)
        # BUTTON - Globals (quick popup)
        elif event == '_GLOBALS_':
            self._display_all_vars(myglobals)
        # BUTTON - clear all
        elif event == 'Clear All Auto Watches':
            if PopupYesNo('Do you really want to clear all Auto-Watches?', 'Really Clear??') == 'Yes':
                self.local_choices = {}
                self.custom_watch = ''
        # BUTTON - Popout
        elif event == '_POPOUT_':
            if not self.popout_window:
                self._build_floating_window()
        # BUTTON - Show All
        elif event == '_SHOW_ALL_':
            for key in self.locals:
                self.local_choices[key] = not key.startswith('_')

        # -------------------- Process the manual "watch list" ------------------
        for i in range(3):
            key = '_VAR{}_'.format(i)
            out_key = '_VAR{}_CHANGED_'.format(i)
            self.myrc = ''
            if self.watcher_window.Element(key):
                var = values[key]
                try:
                    result = eval(str(var), myglobals, mylocals)
                except:
                    result = ''
                self.watcher_window.Element(out_key).Update(str(result))
            else:
                self.watcher_window.Element(out_key).Update('')

        # -------------------- Process the automatic "watch list" ------------------
        slot = 0
        for key in self.local_choices:
            if key == '_CUSTOM_WATCH_':
                continue
            if self.local_choices[key]:
                self.watcher_window.Element('_WATCH{}_'.format(slot)).Update(key)
                try:
                    self.watcher_window.Element('_WATCH{}_RESULT_'.format(slot), silent_on_error=True).Update(mylocals[key])
                except:
                    self.watcher_window.Element('_WATCH{}_RESULT_'.format(slot)).Update('')
                slot += 1

            if slot + int(not self.custom_watch in (None, '')) >= NUM_AUTO_WATCH:
                break
        # If a custom watch was set, display that value in the window
        if self.custom_watch:
            self.watcher_window.Element('_WATCH{}_'.format(slot)).Update(self.custom_watch)
            try:
                self.myrc = eval(self.custom_watch, myglobals, mylocals)
            except:
                self.myrc = ''
            self.watcher_window.Element('_WATCH{}_RESULT_'.format(slot)).Update(self.myrc)
            slot += 1
        # blank out all of the slots not used (blank)
        for i in range(slot, NUM_AUTO_WATCH):
            self.watcher_window.Element('_WATCH{}_'.format(i)).Update('')
            self.watcher_window.Element('_WATCH{}_RESULT_'.format(i)).Update('')

        return True     # return indicating the window stayed open

    ######                                 #     #
    #     #  ####  #####  #    # #####     #  #  # # #    # #####   ####  #    #
    #     # #    # #    # #    # #    #    #  #  # # ##   # #    # #    # #    #
    ######  #    # #    # #    # #    #    #  #  # # # #  # #    # #    # #    #
    #       #    # #####  #    # #####     #  #  # # #  # # #    # #    # # ## #
    #       #    # #      #    # #         #  #  # # #   ## #    # #    # ##  ##
    #        ####  #       ####  #          ## ##  # #    # #####   ####  #    #

    ######                                    #                     #     #
    #     # #    # #    # #####   ####       # #   #      #         #     #   ##   #####   ####
    #     # #    # ##  ## #    # #          #   #  #      #         #     #  #  #  #    # #
    #     # #    # # ## # #    #  ####     #     # #      #         #     # #    # #    #  ####
    #     # #    # #    # #####       #    ####### #      #          #   #  ###### #####       #
    #     # #    # #    # #      #    #    #     # #      #           # #   #    # #   #  #    #
    ######   ####  #    # #       ####     #     # ###### ######       #    #    # #    #  ####
    # displays them into a single text box

    def _display_all_vars(self, dict):
        """

        :param dict: 

        """
        num_cols = 3
        output_text = ''
        num_lines = 2
        cur_col = 0
        out_text = 'All of your Vars'
        longest_line = max([len(key) for key in dict])
        line = []
        sorted_dict = {}
        for key in sorted(dict.keys()):
            sorted_dict[key] = dict[key]
        for key in sorted_dict:
            value = dict[key]
            wrapped_list = textwrap.wrap(str(value), 60)
            wrapped_text = '\n'.join(wrapped_list)
            out_text += '{} - {}\n'.format(key, wrapped_text)
            if cur_col + 1 == num_cols:
                cur_col = 0
                num_lines += len(wrapped_list)
            else:
                cur_col += 1
        ScrolledTextBox(out_text, non_blocking=True)

 #####                                        #     #
#     # #    #  ####   ####   ####  ######    #  #  #   ##   #####  ####  #    #
#       #    # #    # #    # #      #         #  #  #  #  #    #   #    # #    #
#       ###### #    # #    #  ####  #####     #  #  # #    #   #   #      ######
#       #    # #    # #    #      # #         #  #  # ######   #   #      #    #
#     # #    # #    # #    # #    # #         #  #  # #    #   #   #    # #    #
 #####  #    #  ####   ####   ####  ######     ## ##  #    #   #    ####  #    #

#     #                                                       #     #
#     #   ##   #####  #   ##   #####  #      ######  ####     #  #  # # #    #
#     #  #  #  #    # #  #  #  #    # #      #      #         #  #  # # ##   #
#     # #    # #    # # #    # #####  #      #####   ####     #  #  # # # #  #
 #   #  ###### #####  # ###### #    # #      #           #    #  #  # # #  # #
  # #   #    # #   #  # #    # #    # #      #      #    #    #  #  # # #   ##
   #    #    # #    # # #    # #####  ###### ######  ####      ## ##  # #    #

    def _choose_auto_watches(self, my_locals):
        """

        :param my_locals: 

        """
        ChangeLookAndFeel(COLOR_SCHEME)
        num_cols = 3
        output_text = ''
        num_lines = 2
        cur_col = 0
        layout = [[Text('Choose your "Auto Watch" variables', font='ANY 14', text_color='red')]]
        longest_line = max([len(key) for key in my_locals])
        line = []
        sorted_dict = {}
        for key in sorted(my_locals.keys()):
            sorted_dict[key] = my_locals[key]
        for key in sorted_dict:
            line.append(CB(key, key=key, size=(longest_line, 1),
                              default=self.local_choices[key] if key in self.local_choices else False))
            if cur_col + 1 == num_cols:
                cur_col = 0
                layout.append(line)
                line = []
            else:
                cur_col += 1
        if cur_col:
            layout.append(line)

        layout += [
            [Text('Custom Watch (any expression)'), Input(default_text=self.custom_watch, size=(40, 1), key='_CUSTOM_WATCH_')]]
        layout += [
            [Ok(), Cancel(), Button('Clear All'), Button('Select [almost] All', key='_AUTO_SELECT_')]]

        window = Window('All Locals', layout, icon=PSGDebugLogo).Finalize()

        while True:  # event loop
            event, values = window.Read()
            if event in (None, 'Cancel'):
                break
            elif event == 'Ok':
                self.local_choices = values
                self.custom_watch = values['_CUSTOM_WATCH_']
                break
            elif event == 'Clear All':
                PopupQuickMessage('Cleared Auto Watches', auto_close=True, auto_close_duration=3, non_blocking=True,
                                     text_color='red', font='ANY 18')
                for key in sorted_dict:
                    window.Element(key).Update(False)
                window.Element('_CUSTOM_WATCH_').Update('')
            elif event == 'Select All':
                for key in sorted_dict:
                    window.Element(key).Update(False)
            elif event == '_AUTO_SELECT_':
                for key in sorted_dict:
                    window.Element(key).Update(not key.startswith('_'))

        # exited event loop
        window.Close()
        ChangeLookAndFeel('SystemDefault')

    ######                            #######
    #     # #    # # #      #####     #       #       ####    ##   ##### # #    #  ####
    #     # #    # # #      #    #    #       #      #    #  #  #    #   # ##   # #    #
    ######  #    # # #      #    #    #####   #      #    # #    #   #   # # #  # #
    #     # #    # # #      #    #    #       #      #    # ######   #   # #  # # #  ###
    #     # #    # # #      #    #    #       #      #    # #    #   #   # #   ## #    #
    ######   ####  # ###### #####     #       ######  ####  #    #   #   # #    #  ####

    #     #
    #  #  # # #    # #####   ####  #    #
    #  #  # # ##   # #    # #    # #    #
    #  #  # # # #  # #    # #    # #    #
    #  #  # # #  # # #    # #    # # ## #
    #  #  # # #   ## #    # #    # ##  ##
     ## ##  # #    # #####   ####  #    #

    def _build_floating_window(self, location=(None, None)):
        """

        :param location:  (Default value = (None, None))

        """
        if self.popout_window:              # if floating window already exists, close it first
            self.popout_window.Close()
        ChangeLookAndFeel('Topanga')
        num_cols = 2
        width_var = 15
        width_value = 30
        layout = []
        line = []
        col = 0
        self.popout_choices = self.local_choices
        if self.popout_choices == {}:           # if nothing chosen, then choose all non-_ variables
            for key in sorted(self.locals.keys()):
                self.popout_choices[key] = not key.startswith('_')

        width_var = max([len(key) for key in self.popout_choices])
        for key in self.popout_choices:
            if self.popout_choices[key] is True:
                value = str(self.locals.get(key))
                h = min(len(value)//width_value + 1, MAX_LINES_PER_RESULT_FLOATING)
                line += [Text('{}'.format(key), size=(width_var, 1), font=POPOUT_WINDOW_FONT),
                         Text(' = ', font=POPOUT_WINDOW_FONT),
                         Text(value, key=key, size=(width_value, h), font=POPOUT_WINDOW_FONT)]
                if col + 1 < num_cols:
                    line += [VerticalSeparator(), T(' ')]
                col += 1
            if col >= num_cols:
                layout.append(line)
                line = []
                col = 0
        if col != 0:
            layout.append(line)
        layout = [[Column(layout), Column(
            [[Button('', key='_EXIT_', image_data=red_x, button_color=('#282923', '#282923'), border_width=0)]])]]

        self.popout_window = Window('Floating', layout, alpha_channel=0, no_titlebar=True, grab_anywhere=True,
                                           element_padding=(0, 0), margins=(0, 0), keep_on_top=True,
                                       right_click_menu=['&Right', ['Debugger::RightClick', 'Exit::RightClick']], location=location ).Finalize()
        if location == (None, None):
            screen_size = self.popout_window.GetScreenDimensions()
            self.popout_window.Move(screen_size[0] - self.popout_window.Size[0], 0)
        self.popout_window.SetAlpha(1)

        ChangeLookAndFeel('SystemDefault')
        return True

    ######
    #     # ###### ###### #####  ######  ####  #    #
    #     # #      #      #    # #      #      #    #
    ######  #####  #####  #    # #####   ####  ######
    #   #   #      #      #####  #           # #    #
    #    #  #      #      #   #  #      #    # #    #
    #     # ###### #      #    # ######  ####  #    #

    #######
    #       #       ####    ##   ##### # #    #  ####
    #       #      #    #  #  #    #   # ##   # #    #
    #####   #      #    # #    #   #   # # #  # #
    #       #      #    # ######   #   # #  # # #  ###
    #       #      #    # #    #   #   # #   ## #    #
    #       ######  ####  #    #   #   # #    #  ####

    #     #
    #  #  # # #    # #####   ####  #    #
    #  #  # # ##   # #    # #    # #    #
    #  #  # # # #  # #    # #    # #    #
    #  #  # # #  # # #    # #    # # ## #
    #  #  # # #   ## #    # #    # ##  ##
     ## ##  # #    # #####   ####  #    #

    def _refresh_floating_window(self):
        """ """
        if not self.popout_window:
            return
        for key in self.popout_choices:
            if self.popout_choices[key] is True and key in self.locals:
                if key is not None:
                    self.popout_window.Element(key, silent_on_error=True).Update(self.locals.get(key))
        event, values = self.popout_window.Read(timeout=1)
        if event in (None, '_EXIT_', 'Exit::RightClick'):
            self.popout_window.Close()
            self.popout_window = None
        elif event == 'Debugger::RightClick':
            show_debugger_window()


# 888     888                                .d8888b.         d8888 888 888          888      888
# 888     888                               d88P  Y88b       d88888 888 888          888      888
# 888     888                               888    888      d88P888 888 888          888      888
# 888     888 .d8888b   .d88b.  888d888     888            d88P 888 888 888  8888b.  88888b.  888  .d88b.
# 888     888 88K      d8P  Y8b 888P"       888           d88P  888 888 888     "88b 888 "88b 888 d8P  Y8b
# 888     888 "Y8888b. 88888888 888         888    888   d88P   888 888 888 .d888888 888  888 888 88888888
# Y88b. .d88P      X88 Y8b.     888         Y88b  d88P  d8888888888 888 888 888  888 888 d88P 888 Y8b.
#  "Y88888P"   88888P'  "Y8888  888          "Y8888P"  d88P     888 888 888 "Y888888 88888P"  888  "Y8888

# 8888888888                            888    d8b
# 888                                   888    Y8P
# 888                                   888
# 8888888    888  888 88888b.   .d8888b 888888 888  .d88b.  88888b.  .d8888b
# 888        888  888 888 "88b d88P"    888    888 d88""88b 888 "88b 88K
# 888        888  888 888  888 888      888    888 888  888 888  888 "Y8888b.
# 888        Y88b 888 888  888 Y88b.    Y88b.  888 Y88..88P 888  888      X88
# 888         "Y88888 888  888  "Y8888P  "Y888 888  "Y88P"  888  888  88888P'




def show_debugger_window(location=(None, None), *args):
    """

    :param location:  (Default value = (None, None))
    :param *args: 

    """
    if Debugger.debugger is None:
        Debugger.debugger = Debugger()
    debugger = Debugger.debugger
    frame = inspect.currentframe()
    prev_frame = inspect.currentframe().f_back
    # frame, *others = inspect.stack()[1]
    try:
        debugger.locals = frame.f_back.f_locals
        debugger.globals = frame.f_back.f_globals
    finally:
        del frame

    if not debugger.watcher_window:
        debugger.watcher_window = debugger._build_main_debugger_window(location=location)
    return True


def show_debugger_popout_window(location=(None, None), *args):
    """

    :param location:  (Default value = (None, None))
    :param *args: 

    """
    if Debugger.debugger is None:
        Debugger.debugger = Debugger()
    debugger = Debugger.debugger
    frame = inspect.currentframe()
    prev_frame = inspect.currentframe().f_back
    # frame = inspect.getframeinfo(prev_frame)
    # frame, *others = inspect.stack()[1]
    try:
        debugger.locals = frame.f_back.f_locals
        debugger.globals = frame.f_back.f_globals
    finally:
        del frame
    if debugger.popout_window:
        debugger.popout_window.Close()
        debugger.popout_window = None
    debugger._build_floating_window(location=location)


def refresh_debugger():
    """ """
    if Debugger.debugger is None:
        Debugger.debugger = Debugger()
    debugger = Debugger.debugger
    Window.read_call_from_debugger = True
    frame = inspect.currentframe()
    frame = inspect.currentframe().f_back
    # frame, *others = inspect.stack()[1]
    try:
        debugger.locals = frame.f_back.f_locals
        debugger.globals = frame.f_back.f_globals
    finally:
        del frame
    debugger._refresh_floating_window() if debugger.popout_window else None
    rc = debugger._refresh_main_debugger_window(debugger.locals, debugger.globals) if debugger.watcher_window else False
    Window.read_call_from_debugger = False
    return rc







"""
                       d8b          
                       Y8P          

88888b.d88b.   8888b.  888 88888b.  
888 "888 "88b     "88b 888 888 "88b 
888  888  888 .d888888 888 888  888 
888  888  888 888  888 888 888  888 
888  888  888 "Y888888 888 888  888 

"""


def main():
    """ """
    from random import randint

    ChangeLookAndFeel('GreenTan')
    # ------ Menu Definition ------ #
    menu_def = [['&File', ['!&Open', '&Save::savekey', '---', '&Properties', 'E&xit']],
                ['!&Edit', ['!&Paste', ['Special', 'Normal', ], 'Undo'], ],
                ['&Debugger', ['Popout', 'Launch Debugger']],
                ['&Toolbar', ['Command &1', 'Command &2', 'Command &3', 'Command &4']],
                ['&Help', '&About...'], ]

    treedata = TreeData()

    treedata.Insert("", '_A_', 'Tree Item 1', [1, 2, 3], )
    treedata.Insert("", '_B_', 'B', [4, 5, 6], )
    treedata.Insert("_A_", '_A1_', 'Sub Item 1', ['can', 'be', 'anything'], )
    treedata.Insert("", '_C_', 'C', [], )
    treedata.Insert("_C_", '_C1_', 'C1', ['or'], )
    treedata.Insert("_A_", '_A2_', 'Sub Item 2', [None, None])
    treedata.Insert("_A1_", '_A3_', 'A30', ['getting deep'])
    treedata.Insert("_C_", '_C2_', 'C2', ['nothing', 'at', 'all'])

    for i in range(100):
        treedata.Insert('_C_', i, i, [])

    frame1 = [
        [Input('Input Text', size=(25, 1)), ],
        [Multiline(size=(30, 5), default_text='Multiline Input')],
    ]

    frame2 = [
        [Listbox(['Listbox 1', 'Listbox 2', 'Listbox 3'], size=(20, 5))],
        [Combo(['Combo item 1', ], size=(20, 3), text_color='red', background_color='red')],
        [Combo(['Combo item 1', ], size=(20, 3), text_color='red', background_color='red')],
        [Spin([1, 2, 3], size=(4, 3))],
    ]

    frame3 = [
        [Checkbox('Checkbox1', True), Checkbox('Checkbox1')],
        [Radio('Radio Button1', 1), Radio('Radio Button2', 1, default=True, tooltip='Radio 2')],
        [T('', size=(1, 4))],
    ]

    frame4 = [
        [Slider(range=(0, 100), orientation='v', size=(7, 15), default_value=40),
         Slider(range=(0, 100), orientation='h', size=(11, 15), default_value=40), ],
    ]
    matrix = [[str(x * y) for x in range(4)] for y in range(8)]

    frame5 = [
        [Table(values=matrix, headings=matrix[0],
               auto_size_columns=False, display_row_numbers=True, change_submits=False, justification='right',
               num_rows=10, alternating_row_color='lightblue', key='_table_', text_color='black',
               col_widths=[5, 5, 5, 5], size=(400, 200)), T(' '),
         Tree(data=treedata, headings=['col1', 'col2', 'col3'], change_submits=True, auto_size_columns=True,
              num_rows=10, col0_width=10, key='_TREE_', show_expanded=True, )],
    ]

    graph_elem = Graph((800, 150), (0, 0), (800, 300), key='+GRAPH+')

    frame6 = [
        [graph_elem],
    ]

    tab1 = Tab('Graph Number 1', frame6, tooltip='tab 1')
    tab2 = Tab('Graph Number 2', [[]])

    layout1 = [
        [Menu(menu_def)],
        [Image(data=DEFAULT_BASE64_ICON)],
        [Text('You are running the py file itself', font='ANY 15', tooltip='My tooltip', key='_TEXT1_')],
        [Text('You should be importing it rather than running it', font='ANY 15')],
        [Frame('Input Text Group', frame1, title_color='red'),
         Image(data=DEFAULT_BASE64_LOADING_GIF, key='_IMAGE_')],
        [Frame('Multiple Choice Group', frame2, title_color='green'),
         Frame('Binary Choice Group', frame3, title_color='purple', tooltip='Binary Choice'),
         Frame('Variable Choice Group', frame4, title_color='blue')],
        [Frame('Structured Data Group', frame5, title_color='red'), ],
        # [Frame('Graphing Group', frame6)],
        [TabGroup([[tab1, tab2]])],
        [ProgressBar(max_value=800, size=(60, 25), key='+PROGRESS+'), Button('Button'), B('Normal'),
         Button('Exit', tooltip='Exit button')],
    ]

    layout = [[Column(layout1)]]

    window = Window('Window Title', layout,
                    font=('Helvetica', 13),
                    # background_color='black',
                    right_click_menu=['&Right', ['Right', '!&Click', '&Menu', 'E&xit', 'Properties']],
                    # transparent_color= '#9FB8AD',
                    resizable=True,
                    ).Finalize()
    graph_elem.DrawCircle((200, 200), 50, 'blue')
    i = 0
    while True:  # Event Loop
        # TimerStart()
        event, values = window.Read(timeout=0)
        if event != TIMEOUT_KEY:
            print(event, values)
        if event is None or event == 'Exit':
            break
        if i < 800:
            graph_elem.DrawLine((i, 0), (i, randint(0, 300)), width=1, color='#{:06x}'.format(randint(0, 0xffffff)))
        else:
            graph_elem.Move(-1, 0)
            graph_elem.DrawLine((i, 0), (i, randint(0, 300)), width=1, color='#{:06x}'.format(randint(0, 0xffffff)))

        window.FindElement('+PROGRESS+').UpdateBar(i % 800)
        window.Element('_IMAGE_').UpdateAnimation(DEFAULT_BASE64_LOADING_GIF, time_between_frames=50)
        i += 1
        if event == 'Button':
            window.Element('_TEXT1_').SetTooltip('NEW TEXT')
            window.SetTransparentColor('#9FB8AD')
            window.Maximize()
        elif event == 'Normal':
            window.Normal()
        elif event == 'Popout':
            show_debugger_popout_window()
        elif event == 'Launch Debugger':
            show_debugger_window()
        # TimerStop()
    window.Close()


if __name__ == '__main__':
    main()
    exit(69)

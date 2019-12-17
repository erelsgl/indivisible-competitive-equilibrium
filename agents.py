#!python3

"""
A class representing an agent with arbitrary strict preferences.
Preferences are defined by a list of bundles, from best to worst.

AUTHOR: Erel Segal-Halevi
SINCE:  2019-08
"""

class Agent:
    def __init__(self, preferences:list):
        """
        Initialize an agent with strict preferences represented by the given list.
        :param preferences: a list of bundles, from best to worst.
        """
        if type(preferences) is Agent:
            self.preferences = preferences.preferences
        else:
            self.preferences = [''.join(sorted(bundle)) for bundle in preferences]


    def bundles_preferred_to(self, bundle:str):
        """
        Returns all bundles that the agent prefers to the given bundle.
        :param bundle:
        :return: a generator; generates the bundles from the agent's preferences from the top to the given bundle, not including the given bundle.

        >>> a = Agent(["xyz","xy","x","y",""])
        >>> list(a.bundles_preferred_to(""))
        ['xyz', 'xy', 'x', 'y']
        >>> list(a.bundles_preferred_to("y"))
        ['xyz', 'xy', 'x']
        >>> list(a.bundles_preferred_to("x"))
        ['xyz', 'xy']
        >>> list(a.bundles_preferred_to("xy"))
        ['xyz']
        >>> list(a.bundles_preferred_to("yx"))
        ['xyz']
        >>> list(a.bundles_preferred_to("xyz"))
        []
        >>> list(a.bundles_preferred_to("zyx"))
        []
        >>> a = Agent(reversed(["xyz", "xy","x","y",""]))
        >>> list(a.bundles_preferred_to(""))
        []
        >>> list(a.bundles_preferred_to("x"))
        ['', 'y']
        >>> list(a.bundles_preferred_to("xy"))
        ['', 'y', 'x']
        >>> list(a.bundles_preferred_to("yx"))
        ['', 'y', 'x']
        """
        bundle = ''.join(sorted(bundle))
        for other_bundle in self.preferences:
            if other_bundle==bundle:
                return
            yield other_bundle

    @staticmethod
    def profile(preferences:list):
        """
        Convert the given list of preferences to a list of agents.
        :param preferences: a list of lists of strings, each of which represents strict preferences of a single agent.
        :return: a list of Agent objects.
        """
        if type(preferences[0]) is Agent:
            return preferences   # it is already a list of agents - no need to convert.
        else:
            profile = []
            for pref in preferences:
                agent = Agent(pref)
                if len(agent.preferences)==0:
                    raise ValueError("Empty preference list for pref {}".format(pref))
                profile.append(agent)
            return profile


if __name__ == "__main__":
    import doctest
    (failures,tests) = doctest.testmod(report=True)
    print ("{} failures, {} tests".format(failures,tests))

class ConversationMemory:
    def __init__(self):
        self.base_query = ""
        self.refinements = []

    def start(self, initial_query):
        self.base_query = initial_query
        self.refinements = []

    def update(self, follow_up):
        self.refinements.append(follow_up)

    def get_combined_query(self):
        if not self.refinements:
            return self.base_query
        return self.base_query + ", " + ", ".join(self.refinements)

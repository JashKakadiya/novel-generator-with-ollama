#from utils import BaseStructureChain, ChatOpenAI
#from utils import BaseStructureChain, LlamaCpp
from utils import BaseStructureChain, Ollama


class TitleChain(BaseStructureChain):

    PROMPT = """
    Your job is to generate the title for a novel about the following subject and main character. 
    Return a title and only a title!
    The title should be consistent with the genre of the novel.
    The title should be consistent with the style of the author.

    Subject: {subject}
    Genre: {genre}
    Author: {author}

    Main character's profile: {profile}

    Title:"""

    def run(self, subject, genre, author, profile):
        return self.chain.predict(
            subject=subject,
            genre=genre,
            author=author,
            profile=profile
        )
    

class PlotChain(BaseStructureChain):

    PROMPT = """
    Your job is to generate the plot for a novel. Return a plot and only a plot!
    Describe the full plot of the story and don't hesitate to create new characters to make it compelling.
    You are provided the following subject, title and main character's profile.
    Make sure that the main character is at the center of the story 
    The plot should be consistent with the genre of the novel.
    The plot should be consistent with the style of the author.

    Consider the following attributes to write an exciting story:
    {features}

    subject: {subject}
    Genre: {genre}
    Author: {author}

    Title: {title}
    Main character's profile: {profile}

    Plot:"""

    HELPER_PROMPT = """
    Generate a list of attributes that characterized an exciting story.

    List of attributes:"""
    
    def run(self, subject, genre, author, profile, title):
        features = Ollama().predict(self.HELPER_PROMPT)    
#        features = LlamaCpp().predict(self.HELPER_PROMPT)
#        features = ChatOpenAI().predict(self.HELPER_PROMPT)

        plot = self.chain.predict(
            features=features,
            subject=subject,
            genre=genre,
            author=author,
            profile=profile,
            title=title
        )

        return plot
    

class ChaptersChain(BaseStructureChain):

    PROMPT = """
    Your job is to generate a list of chapters. 
    ONLY the list and nothing more!
    You are provided with a title, a plot and a main character for a novel.
    Generate a list of chapters describing the plot of that novel.
    Make sure the chapters are consistent with the plot.
    The chapters should be consistent with the genre of the novel. 
    The chapters should be consistent with the style of the author. 

    Follow this template: 

    Prologue: [description of prologue]
    Chapter 1: [description of chapter 1]
    ...
    Epilogue: [description of epilogue]

    Make sure the chapter is followed by the character `:` and its description. For example: `Chapter 1: [description of chapter 1]`
    
    subject: {subject}
    Genre: {genre}
    Author: {author}

    Title: {title}
    Main character's profile: {profile}

    Plot: {plot}
    
    Return the chapter list and only the chapter list
    Chapters list:"""
    
    def run(self, subject, genre, author, profile, title, plot):
        response = self.chain.predict(
            subject=subject,
            genre=genre,
            author=author,
            profile=profile,
            title=title,
            plot=plot
        )

        return self.parse(response)

    def parse(self, response):
        chapter_list = response.strip().split('\n')
        chapter_list = [chapter for chapter in chapter_list if ':' in chapter]
        chapter_dict = dict([
            chapter.strip().split(':') 
            for chapter in chapter_list
        ])

        return chapter_dict
    

def get_structure(subject, genre, author, profile):

    title_chain = TitleChain()
    plot_chain = PlotChain()
    chapters_chain = ChaptersChain()

    title = title_chain.run(
        subject, 
        genre, 
        author, 
        profile
    )
    plot = plot_chain.run(
        subject, 
        genre, 
        author, 
        profile, 
        title
    )
    chapter_dict = chapters_chain.run(
        subject, 
        genre, 
        author, 
        profile, 
        title, 
        plot
    )

    return title, plot, chapter_dict

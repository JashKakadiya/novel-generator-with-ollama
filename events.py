from utils import BaseEventChain, Ollama

class ChapterPlotChain(BaseEventChain):

    HELPER_PROMPT = """
    Generate a list of attributes that characterized an exciting story.

    List of attributes:"""

    PROMPT = """
    You are a writer and your job is to generate the plot for one and only one chapter of a novel. 
    You are provided with the title, the main plot of the novel and the main character.
    Additionally, you are provided with the plots of the previous chapters and the outline of the novel.
    Make sure to generate a plot that describe accurately the story of the chapter. 
    Each chapter should have its own arc, but should be consistent with the other chapters and the overall story.
    The summary should be consistent with the genre of the novel.
    The summary should be consistent with the style of the author. 

    Consider the following attributes to write an exciting story:
    {features}

    subject: {subject}
    Genre: {genre}
    Author: {author}

    Title: {title}
    Main character's profile: {profile}

    Novel's Plot: {plot}

    Outline:
    {outline}

    Chapter Plots:
    {summaries}

    Return the plot and only the plot
    Plot of {chapter}:"""

    def run(self, subject, genre, author, profile, title,
            plot, summaries_dict, chapter_dict, chapter):
        
        features = Ollama().predict(self.HELPER_PROMPT)
#        features = LlamaCpp().predict(self.HELPER_PROMPT)
#        features = ChatOpenAI().predict(self.HELPER_PROMPT)

        outline = '\n'.join([
            '{} - {}'.format(chapter, description)
            for chapter, description in chapter_dict.items()
        ])

        summaries = '\n\n'.join([
            'Plot of {}: {}'.format(chapter, summary)
            for chapter, summary in summaries_dict.items()
        ])

        return self.chain.predict(
            subject=subject,
            genre=genre,
            author=author,
            profile=profile,
            title=title,
            plot=plot,
            features=features,
            outline=outline,
            summaries=summaries,
            chapter=chapter
        )
    

class EventsChain(BaseEventChain):

    PROMPT = """
    You are a writer and your job is to come up with a detailled list of events happens in the current chapter of a novel.
    Those events describes the plot of that chapter and the actions of the different characters in chronological order. 
    You are provided with the title, the main plot of the novel, the main character, and a summary of that chapter.
    Additionally, you are provided with the list of the events that were outlined in the previous chapters.
    The event list should be consistent with the genre of the novel.
    The event list should be consistent with the style of the author.

    The each element of that list should be returned on different lines. Follow this template:

    Event 1
    Event 2
    ...
    Final event

    subject: {subject}
    Genre: {genre}
    Author: {author}

    Title: {title}
    Main character's profile: {profile}

    Novel's Plot: {plot}

    Events you outlined for previous chapters: {previous_events}

    Summary of the current chapter:
    {summary}

    Return the events and only the events!
    Event list for that chapter:"""
    
    def run(self, subject, genre, author, profile, 
            title, plot, summary, event_dict):
        
        previous_events = ''
        for chapter, events in event_dict.items():
            previous_events += '\n' + chapter
            for event in events:
                previous_events += '\n' + event

        response = self.chain.predict(
            subject=subject,
            genre=genre,
            author=author,
            profile=profile,
            title=title,
            plot=plot,
            summary=summary,
            previous_events=previous_events,
        )

        return self.parse(response)
    
    def parse(self, response):

        event_list = response.strip().split('\n')
        event_list = [
            event.strip() for event in event_list if event.strip()
        ]
        return event_list
    

def get_events(subject, genre, author, profile, title, plot, chapter_dict):
    chapter_plot_chain = ChapterPlotChain()
    events_chain = EventsChain()
    summaries_dict = {}
    event_dict = {}

    for chapter, _ in chapter_dict.items():

        summaries_dict[chapter] = chapter_plot_chain.run(
            subject=subject, 
            genre=genre, 
            author=author, 
            profile=profile, 
            title=title, 
            plot=plot, 
            summaries_dict=summaries_dict, 
            chapter_dict=chapter_dict, 
            chapter=chapter
        )

        event_dict[chapter] = events_chain.run(
            subject=subject, 
            genre=genre, 
            author=author, 
            profile=profile, 
            title=title, 
            plot=plot, 
            summary=summaries_dict[chapter], 
            event_dict=event_dict
        )

    return summaries_dict, event_dict

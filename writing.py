from utils import BaseEventChain


class WriterChain(BaseEventChain):

    PROMPT = """
    You are a novel writer. The novel is described by a list of events. 
    You have already written the novel up to the last event. 
    Your job is to generate the paragraphs of the novel about the new event.
    You are provided with a the title, the novel's plot, a description of the main character and a plot of the current chapter.
    Make sure the paragraphs are consistent with the plot of the chapter.
    Additionally you are provided with the list of events you have already written about.
    The paragraphs should be consistent with the genre of the novel.
    The paragraphs should be consistent with the style of the author.

    Genre: {genre}
    Author: {author}

    Title: {title}
    Main character's profile: {profile}

    Novel's Plot: {plot}

    Previous events:
    {previous_events}

    Current Chapter summary: {summary}

    Previous paragraphs:
    {previous_paragraphs}

    New event you need to write about now: 
    {current_event}

    Paragraphs of the novel describing that event:"""

    def run(self, genre, author, title, profile, plot, 
            previous_events, summary, previous_paragraphs, current_event):

        previous_events = '\n'.join(previous_events)

        return self.chain.predict(
            genre=genre, 
            author=author, 
            title=title, 
            profile=profile, 
            plot=plot, 
            previous_events=previous_events, 
            summary=summary,
            previous_paragraphs=previous_paragraphs, 
            current_event=current_event
        )
    
def write_book(genre, author, title, profile, plot, summaries_dict, event_dict):
    
    writer_chain = WriterChain()
    previous_events = []
    book = {}
    paragraphs = ''

    for chapter, event_list in event_dict.items():

        book[chapter] = []

        for event in event_list:

            paragraphs = writer_chain.run(
                genre=genre, 
                author=author, 
                title=title, 
                profile=profile, 
                plot=plot, 
                previous_events=previous_events, 
                summary=summaries_dict[chapter], 
                previous_paragraphs=paragraphs, 
                current_event=event
            )

            previous_events.append(event)
            book[chapter].append(paragraphs)

    return book

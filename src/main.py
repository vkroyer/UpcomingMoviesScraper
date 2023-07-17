from mail import format_mail, send_email
from markdown import markdown
from notion_class import NotionUpdater
from requests_session import RateLimitedSession
from scrape import find_upcoming_projects

TMDB_MAX_REQUESTS_PER_SECOND = 30
NOTION_MAX_REQUESTS_PER_SECOND = 3

def main():

    with RateLimitedSession(max_requests=TMDB_MAX_REQUESTS_PER_SECOND) as tmdb_session:
        with RateLimitedSession(max_requests=NOTION_MAX_REQUESTS_PER_SECOND) as notion_session:
            
            notion_updater = NotionUpdater(session=notion_session)

            new_projects = []

            # TODO: Move projects that have been released to the Released Projects database
            # Scrape new upcoming projects from all persons
            for person in notion_updater.person_list:
                
                projects = find_upcoming_projects(requests_session=tmdb_session, person=person)
                
                for project in projects:
                    # Check if project is already in the database
                    if project.tmdb_id in person.projects:
                        continue

                    # Check if the project is already in another person's list
                    used_tmdb_ids = [project.tmdb_id for project in new_projects]
                    if project.tmdb_id in used_tmdb_ids:

                        # Update the project with the new person
                        used_project = new_projects[used_tmdb_ids.index(project.tmdb_id)]
                        used_project.associated_person_page_ids.append(person.notion_page_id)
                        person.projects.append(project.tmdb_id)
                        continue

                    new_projects.append(project)
                    person.projects.append(project.tmdb_id)

            notion_updater.add_upcoming_projects_to_database(projects=new_projects)
    
    notion_updater.update_json_files()


    # mail_content_markdown = format_mail(notion_updater=notion_updater)
    # mail_content_html = markdown(mail_content_markdown)

    # subject = "Roundup of Upcoming Movies and TV Shows"
    # send_email(subject=subject, content=mail_content_html)

    notion_updater.close()
    

if __name__ == "__main__":
    import time
    start = time.time()
    main()
    stop = time.time()
    print(f"Done in {round(stop-start, 2)} s")
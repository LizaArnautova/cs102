<!DOCTYPE html>
<html>
    <head>
        <link rel="stylesheet" href="//cdnjs.cloudflare.com/ajax/libs/semantic-ui/2.2.12/semantic.min.css"></link>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/jquery/3.1.1/jquery.min.js"></script>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/semantic-ui/2.2.12/semantic.min.js"></script>
    </head>
    <body>
    <h2><center>Hacker News</center></h2>
        <div class="ui container" style="padding-top: 10px;">
        <table class="ui celled table">
            <thead class="full-width">
                <tr>
                    <th colspan="7">
                        <a href="/news" class="ui  floated small  button">Return to the main page</a>
                        <a href="/classify" class="ui  floated small primary button">Get predictions</a>
                        <a href="/all" class="ui  floated small primary button">See rated news</a>
                        <a href="/update" class="ui right floated small primary button">More Hacker News!</a>
                    </th>
                </tr>
            </thead>
            <thead>
                <th>Title</th>
                <th>Author</th>
                <th>Likes</th>
                <th>Comments</th>
                <th colspan="3">Label</th>
            </thead>
            <tbody>
                %for row in rows:
                <tr>
                    <td><a href="{{ row.url }}">{{ row.title }}</a></td>
                    <td>{{ row.author }}</td>
                    <td>{{ row.points }}</td>
                    <td>{{ row.comments }}</td>
                    <td class="positive"><a href="/add_label/?label=good&id={{ row.id }}">Interested</a></td>
                    <td class="active"><a href="/add_label/?label=maybe&id={{ row.id }}">Maybe</a></td>
                    <td class="negative"><a href="/add_label/?label=never&id={{ row.id }}">Not interested</a></td>
                </tr>
                %end
            </tbody>
            <tfoot class="full-width">
                <tr>
                    <th colspan="7">
                        <a href="/news" class="ui  floated small  button">Return to the main page</a>
                        <a href="/classify" class="ui  floated small primary button">Get predictions</a>
                        <a href="/all" class="ui  floated small primary button">See rated news</a>
                        <a href="/update" class="ui right floated small primary button">More Hacker News!</a>
                    </th>
                </tr>
            </tfoot>
        </table>
        </div>
    </body>
</html>
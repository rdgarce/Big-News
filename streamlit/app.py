import streamlit as st

def main():
    st.title("Visualizzazione del Grafo")

    # Codice HTML/JavaScript del grafo
    graph_html = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Graph Visualization</title>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/vis/4.21.0/vis.min.js"></script>
        <link href="https://cdnjs.cloudflare.com/ajax/libs/vis/4.21.0/vis.min.css" rel="stylesheet" type="text/css">
        <style>
            #graph-container {
                width: 100%;
                height: 500px;
                border: 1px solid lightgray;
            }
        </style>
    </head>
    <body>
        <div id="graph-container"></div>

        <script type="text/javascript">
            // Creazione di un grafo di esempio
            var nodes = new vis.DataSet([
                { id: 1, label: 'Node 1' },
                { id: 2, label: 'Node 2' },
                { id: 3, label: 'Node 3' },
                { id: 4, label: 'Node 4' },
                { id: 5, label: 'Node 5' }
            ]);

            var edges = new vis.DataSet([
                { from: 1, to: 2 },
                { from: 1, to: 3 },
                { from: 2, to: 4 },
                { from: 2, to: 5 },
                { from: 3, to: 4 }
            ]);

            var container = document.getElementById('graph-container');
            var data = {
                nodes: nodes,
                edges: edges
            };
            var options = {};
            var network = new vis.Network(container, data, options);
        </script>
    </body>
    </html>
    """

    # Utilizzo di st.components.html per incorporare il grafo nel layout di Streamlit
    st.html(graph_html)

if __name__ == "__main__":
    main()

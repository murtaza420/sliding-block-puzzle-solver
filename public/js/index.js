// Builds the layout of the puzzle based on the dimensions
const buildPuzzle = () => {
    $('#error-message-1').addClass("d-none")
    $('#puzzle-board').html("")
    $('#puzzle-solve').addClass("d-none")
    $('#results').addClass('d-none')

    const dimensions = $('#dimensions').val()

    if (!validDimensions(dimensions)) {
        $('#error-message-1').removeClass("d-none")
        return
    }
    const [x,y] = dimensions.split(",")
    
    let count = 1
    let temp = ""
    for(i = 0; i < y; i++){
        temp += '<div class="puzzle-row">'
        for(j = 0; j < x; j++){
            temp += buildSquare(count)
            count++;
        }
        temp += "</div><br/>"
    }
    $('#puzzle-board').html(temp)
    $('#puzzle-solve').removeClass("d-none")
}

// Builds individual input squares
const buildSquare = id => '<input class="puzzle-item" id="' + id + '" onchange="inputChangeHandler(this.id)" type="number"/>'

// Builds the individual squares for final state
const buildResultSquare = value => {
    const color = getColor(value)
    return '<input class="puzzle-item ' +  color + '" value="' + value + '" disabled/>'
}

// Validates the dimensions
const validDimensions = dimensions => {
    dim = dimensions.split(",")
    if (dim.length != 2) {
        return false
    }
    return true
}

// Resets the solutions 
// Makes the Rest API call
const solvePuzzle = async () => {
    $('#error-message-2').addClass("d-none")

    body = {
        dimensions: $('#dimensions').val()
    }
    const items = $('.puzzle-item')

    // Checks if all input squares are filled
    for(i = 0; i < items.length; i++){
        if (items[i].value == '') {
            $('#error-message-2').removeClass("d-none")
            return
        }
        
        body[items[i].getAttribute('id')] = items[i].value
    }

    try {
        resetSolution()
        const response = await fetch('/solve_puzzle', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json;charset=utf-8'
            },
            body: JSON.stringify(body)
        })

        $('#solving').addClass("d-none")
        const output = await response.json()
        renderOutput(output)  
    } catch (error) {
        console.log('ERROR',error)   
    }
}

// Resetting the content of previous solution
const resetSolution = () => {
    $('#solving').removeClass("d-none")
    $('#results').removeClass('d-none')
    $('#bfs-time').text("")
    $('#dfs-time').text("")
    $('#idfs-time').text("")
    $('#bfs-final-state').html("")
    $('#dfs-final-state').html("")
    $('#idfs-final-state').html("")
    $('#bfs-moves').html("")
    $('#dfs-moves').html("")
    $('#idfs-moves').html("")
}

// Renders output to HTML
const renderOutput = output => {
    const {bfs, dfs, idfs} = output

    // Render Time
    $('#bfs-time').text('Time: ' + bfs.time + 's')
    $('#dfs-time').text('Time: ' + dfs.time + 's')
    $('#idfs-time').text('Time: ' + idfs.time + 's')
    
    // Build Final State
    const bfsFinalState = getFinalState(bfs['final_state'])
    const dfsFinalState = getFinalState(dfs['final_state'])
    const idfsFinalState = getFinalState(idfs['final_state'])

    // Render Final State
    $('#bfs-final-state').html(bfsFinalState)
    $('#dfs-final-state').html(dfsFinalState)
    $('#idfs-final-state').html(idfsFinalState)

    // Build List Moves
    const bfsMoves = getMovesList(bfs['moves'])
    const dfsMoves = getMovesList(dfs['moves'])
    const idfsMoves = getMovesList(idfs['moves'])

    // Render List Moves
    $('#bfs-moves').html(bfsMoves)
    $('#dfs-moves').html(dfsMoves)
    $('#idfs-moves').html(idfsMoves)
}

// Builds the final state
const getFinalState = stateDict => {
    const dimensions = $('#dimensions').val()
    const [x, y] = dimensions.split(",")
    let finalState = ""
    let pos = 1
    for(i = 0; i < y; i++){
        finalState += '<div class="puzzle-row">'
        for(j = 0; j < x; j++){
            finalState += buildResultSquare(stateDict[pos + ''])
            pos += 1
        }
        finalState += '</div><br>'
    }
    return finalState
}

// Builds the moves list
const getMovesList = moves => moves.map(move => '<li>' + move + '</li>')

// Updates background color of the square when input changes
const inputChangeHandler = id => {
    const value = $('#' + id).val()
    const element = $('#' + id)
    const classes = element.attr('class').split(' ')

    classes.map(c => {
        if (c != 'puzzle-item') {
            element.removeClass(c)
        }
    })

    const color = getColor(value)
    element.addClass(color)
}

// Maps the color to the input value
const getColor = value => {
    if (value == -1) {
        return "green"
    }
    else if (value == 2) {
        return "red"
    }
    else if (value == 0) {
        return "white"
    }
    else if (value == 1) {
        return "grey"
    }
    else if (value > 2) {
        return "yellow"
    }
}
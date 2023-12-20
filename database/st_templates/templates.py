photo_template = """
<div>
        <h1>IoT Counting System</h1>
    </div>
    <div>
        <h2>About us</h2>
        <ul>
            <li>This product supports library on managing and lending IoT kits.</li>
            <li>Let's say you are a library admin, you are lending kits to students.</li>
            <li>Here, you can use this system to count objects, then save records for borrows and returns.</li>
        </ul>
    </div>
    <div>
        <h2>How to use?</h2>
    <h3>1. First, prepare a photo of the IoT objects.</h3>
    <h4>Tips to take a good photo</h4>
    <ul>
        <li> First find a table top that has: of soft color background.
            <ul>
                <li>Soft color background(e.g. wooden brown)</li>
                <li>Has multiple light sources (e.g. Classroom lighting, Library lighting).</li>
            </ul>
        </li>
        <li>Scatter objects onto a table top so that: No overlapping objects.</li>
        <li>Take a photo:
            <ul>
                <li>Your camera should be parallel and 50-70 cm above the table's surface.</li>
                <li>Hold steady to avoid any blur in the photo.</li>
            </ul>
        </li>
    </ul>
    </div>
"""

process_template = """
<div>
        <h3>2.a. Then, go to <a href="/Borrow" target="_self">Borrow</a> to count and save a Borrow record assigned to a Student.</h3>
        <h4>Instruction on Borrow tab</h4>   
        <ul>
            <li>Enter the student's ID</li>
            <li>Upload the photo</li>
            <li>Click Get Result</li>
        </ul>
        <h4 style="font-weight: normal;">After seeing the result, you can:
        </h4>
        <ul><li>Overwrite results and Click 'Update result' to save a record.</li></ul>
    </div>
    <div>
        <h3>2.b. Or, go to <a href="/Return" target="_self">Return</a> to count and save a Return record (only accessible if Student has active Borrow record)</h3>
        <h4>Instruction on Return table</h4>
        <ul>
            <li>Enter the student's ID</li>
            <li>Upload the photo</li>
            <li>Click Get Result</li>
        </ul>
        <h4 style="font-weight: normal;">After seeing the result, you can:
        </h4>
        <ul>
            <li>Overwrite results and Click 'Update result' to save record.</li>
            <li>Click 'Show borrow image' to see the photo of the student's borrow record.
            </li>
        </ul>
    </div>
"""
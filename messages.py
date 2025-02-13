from animation import draw_better_heart

def show_final_message(canvas):
    """
    Displays the final loving message and extra decorative hearts on the canvas.
    
    :param canvas: The tkinter canvas on which to display the message.
    """
    width = int(canvas['width'])
    height = int(canvas['height'])
    canvas.create_text(width/2, height/2 - 100,
                       text="Happy Valentine's Day!",
                       font=("Helvetica", 36, "bold"),
                       fill="white")
    canvas.create_text(width/2, height/2 - 40,
                       text="I love you so much!",
                       font=("Helvetica", 28),
                       fill="white")
    positions = [
        (width/2 - 200, height/2 + 100),
        (width/2 - 100, height/2 + 150),
        (width/2,     height/2 + 100),
        (width/2 + 100, height/2 + 150),
        (width/2 + 200, height/2 + 100)
    ]
    for (x, y) in positions:
        draw_better_heart(canvas, x, y, 30)

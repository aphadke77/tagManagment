import sqlite3
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, simpledialog
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd

class TagManagementApp:
    def __init__(self, root):
        self.root = root  # Correctly assign root as an instance attribute
        self.root.title("Tag Management Application")
        
        # Database connection
        self.conn = sqlite3.connect('tags_database.db')
        
        # Setup UI components
        self.setup_ui()
        self.setup_delete_context_menu()
        
        # Other initialization code...

    def setup_delete_context_menu(self):
        # Create context menu for delete functionality
        self.context_menu = tk.Menu(self.root, tearoff=0)
        self.context_menu.add_command(label="Delete Tag", command=self.delete_selected_tag)
        
        # Bind right-click to show context menu
        def show_context_menu(event):
            self.context_menu.tk_popup(event.x_root, event.y_root)
        
        self.tag_tree.bind("<Button-3>", show_context_menu)

    def delete_selected_tag(self):
        # Get selected item
        selected_item = self.tag_tree.selection()
        
        if not selected_item:
            messagebox.showwarning("Delete Tag", "Please select a tag to delete")
            return
        
        # Confirm deletion
        confirm = messagebox.askyesno("Confirm Deletion", 
            "Are you sure you want to delete the selected tag?")
        
        if confirm:
            # Get the full tag from selected item
            full_tag = self.tag_tree.item(selected_item)['values'][-1]
            
            # Delete from database
            cursor = self.conn.cursor()
            cursor.execute('DELETE FROM tags WHERE full_tag = ?', (full_tag,))
            self.conn.commit()
            
            # Refresh tag list and chart
            self.refresh_tag_list()
            self.update_completeness_chart()
            
            messagebox.showinfo("Delete Tag", "Tag deleted successfully")

    def delete_tags_by_discipline(self):
        # Prompt user to select discipline to delete
        disciplines = ['Mechanical', 'Electrical', 'Instrumentation', 'Process']
        discipline = simpledialog.askstring("Delete Tags", 
            "Enter discipline to delete tags:", 
            initialvalue=disciplines[0])
        
        if discipline and discipline in disciplines:
            # Confirm deletion
            confirm = messagebox.askyesno("Confirm Deletion", 
                f"Are you sure you want to delete ALL tags in {discipline} discipline?")
            
            if confirm:
                # Delete tags from selected discipline
                cursor = self.conn.cursor()
                cursor.execute('DELETE FROM tags WHERE discipline = ?', (discipline,))
                deleted_count = cursor.rowcount
                self.conn.commit()
                
                # Refresh UI
                self.refresh_tag_list()
                self.update_completeness_chart()
                
                messagebox.showinfo("Delete Tags", 
                    f"Deleted {deleted_count} tags in {discipline} discipline")

    def setup_ui(self):
        # Create main frames and widgets
        tag_frame = ttk.Frame(self.root)
        tag_frame.pack(padx=10, pady=10)
        
        # Create Treeview for tags
        self.tag_tree = ttk.Treeview(tag_frame, columns=('Discipline', 'Tag'), show='headings')
        self.tag_tree.grid(row=0, column=0, columnspan=2)
        
        # Add delete buttons
        delete_tag_button = ttk.Button(tag_frame, text="Delete Selected Tag", 
            command=self.delete_selected_tag)
        delete_tag_button.grid(row=7, column=0)
        
        delete_discipline_button = ttk.Button(tag_frame, text="Delete by Discipline", 
            command=self.delete_tags_by_discipline)
        delete_discipline_button.grid(row=7, column=1)

    def refresh_tag_list(self):
        # Placeholder for refreshing tag list
        pass

    def update_completeness_chart(self):
        # Placeholder for updating completeness chart
        pass

    def __del__(self):
        # Close database connection when object is deleted
        if hasattr(self, 'conn'):
            self.conn.close()

def main():
    root = tk.Tk()
    app = TagManagementApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
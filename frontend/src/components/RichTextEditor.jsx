import React, { useMemo, useState } from 'react'
import { createEditor, Transforms, Editor, Element as SlateElement } from 'slate'
import { Slate, Editable, withReact } from 'slate-react'
import { withHistory } from 'slate-history'
import '../styles/RichTextEditor.css'

const RichTextEditor = ({ value, onChange, onAutosave }) => {
  const editor = useMemo(() => withHistory(withReact(createEditor())), [])
  const [format, setFormat] = useState({
    bold: false,
    italic: false,
    underline: false,
    highlight: false,
    fontSize: '16px',
    fontFamily: 'Arial',
  })

  const toggleMark = (format) => {
    const isActive = isMarkActive(editor, format)
    if (isActive) {
      Editor.removeMark(editor, format)
    } else {
      Editor.addMark(editor, format, true)
    }
  }

  const isMarkActive = (editor, format) => {
    const marks = Editor.marks(editor)
    return marks ? marks[format] === true : false
  }

  const isBlockActive = (editor, format) => {
    const { selection } = editor
    if (!selection) return false

    const [match] = Editor.nodes(editor, {
      at: Editor.unhangRange(editor, selection),
      match: (n) =>
        !Editor.isEditor(n) &&
        SlateElement.isElement(n) &&
        n.type === format,
    })
    return !!match
  }

  const toggleBlock = (format) => {
    const isActive = isBlockActive(editor, format)
    const isList = ['numbered-list', 'bulleted-list'].includes(format)

    Transforms.unwrapNodes(editor, {
      match: (n) =>
        !Editor.isEditor(n) &&
        SlateElement.isElement(n) &&
        ['numbered-list', 'bulleted-list', 'list-item'].includes(n.type),
      split: true,
    })

    let newProperties
    if (isActive) {
      newProperties = {
        type: 'paragraph',
      }
    } else if (isList) {
      newProperties = {
        type: 'list-item',
      }
      Transforms.setNodes(editor, newProperties)
      const block = { type: format, children: [] }
      Transforms.wrapNodes(editor, block)
      return
    } else {
      newProperties = {
        type: format,
      }
    }
    Transforms.setNodes(editor, newProperties)
  }

  const handleChangeFontFamily = (font) => {
    Transforms.setNodes(
      editor,
      { fontFamily: font },
      { match: (n) => Editor.isEditor(n) || SlateElement.isElement(n) }
    )
  }

  const renderElement = (props) => {
    const { attributes, children, element } = props
    const style = {
      fontFamily: element.fontFamily || 'Arial',
      fontSize: element.fontSize || '16px',
    }

    switch (element.type) {
      case 'heading':
        return <h2 style={style} {...attributes}>{children}</h2>
      case 'bulleted-list':
        return <ul style={style} {...attributes}>{children}</ul>
      case 'numbered-list':
        return <ol style={style} {...attributes}>{children}</ol>
      case 'list-item':
        return <li style={style} {...attributes}>{children}</li>
      default:
        return <p style={style} {...attributes}>{children}</p>
    }
  }

  const renderLeaf = (props) => {
    let { attributes, children, leaf } = props

    if (leaf.bold) {
      children = <strong>{children}</strong>
    }
    if (leaf.italic) {
      children = <em>{children}</em>
    }
    if (leaf.underline) {
      children = <u>{children}</u>
    }
    if (leaf.highlight) {
      children = <mark style={{ backgroundColor: '#ffd700' }}>{children}</mark>
    }

    return <span {...attributes}>{children}</span>
  }

  return (
    <div className="rich-text-editor">
      <div className="editor-toolbar">
        <div className="toolbar-group">
          <button
            className={`toolbar-btn ${isMarkActive(editor, 'bold') ? 'active' : ''}`}
            onMouseDown={(e) => {
              e.preventDefault()
              toggleMark('bold')
            }}
            title="Bold"
          >
            <strong>B</strong>
          </button>
          <button
            className={`toolbar-btn ${isMarkActive(editor, 'italic') ? 'active' : ''}`}
            onMouseDown={(e) => {
              e.preventDefault()
              toggleMark('italic')
            }}
            title="Italic"
          >
            <em>I</em>
          </button>
          <button
            className={`toolbar-btn ${isMarkActive(editor, 'underline') ? 'active' : ''}`}
            onMouseDown={(e) => {
              e.preventDefault()
              toggleMark('underline')
            }}
            title="Underline"
          >
            <u>U</u>
          </button>
          <button
            className={`toolbar-btn ${isMarkActive(editor, 'highlight') ? 'active' : ''}`}
            onMouseDown={(e) => {
              e.preventDefault()
              toggleMark('highlight')
            }}
            title="Highlight"
          >
            ◆
          </button>
        </div>

        <div className="toolbar-group">
          <select
            className="toolbar-select"
            onChange={(e) => handleChangeFontFamily(e.target.value)}
            defaultValue="Arial"
          >
            <option value="Arial">Arial</option>
            <option value="Georgia">Georgia</option>
            <option value="Courier New">Courier</option>
            <option value="Times New Roman">Times</option>
            <option value="Trebuchet MS">Trebuchet</option>
          </select>
        </div>

        <div className="toolbar-group">
          <button
            className={`toolbar-btn ${isBlockActive(editor, 'bulleted-list') ? 'active' : ''}`}
            onMouseDown={(e) => {
              e.preventDefault()
              toggleBlock('bulleted-list')
            }}
            title="Bullet List"
          >
            •
          </button>
          <button
            className={`toolbar-btn ${isBlockActive(editor, 'numbered-list') ? 'active' : ''}`}
            onMouseDown={(e) => {
              e.preventDefault()
              toggleBlock('numbered-list')
            }}
            title="Numbered List"
          >
            #
          </button>
        </div>
      </div>

      <Slate
        editor={editor}
        value={value}
        onChange={(value) => {
          onChange(value)
          onAutosave?.(value)
        }}
      >
        <Editable
          renderElement={renderElement}
          renderLeaf={renderLeaf}
          className="editor-content"
          placeholder="Start taking notes..."
        />
      </Slate>
    </div>
  )
}

export default RichTextEditor

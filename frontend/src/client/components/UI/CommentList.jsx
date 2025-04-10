import React from "react";

const CommentList = ({ comments }) => {
  return (
    <div
      style={{
        maxHeight: '400px', // chiều cao cố định để hiển thị thanh kéo
        overflowY: 'auto',
        paddingRight: '8px',
        border: '1px solid #ccc',
        borderRadius: '8px',
      }}
    >
      {comments.map((comment) => (
        <div
          key={comment.id}
          style={{
            marginBottom: '16px',
            padding: '8px',
            borderBottom: '1px solid #ccc',
            color: '#000',
          }}
        >
          <strong>{comment.author}</strong> ({comment.date})<br />
          <p>{comment.content}</p>
        </div>
      ))}
    </div>
  );
};

export default CommentList;

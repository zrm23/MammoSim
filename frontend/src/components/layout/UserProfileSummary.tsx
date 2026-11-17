import "../../styles/Header.css";

type UserProfileSummaryProps = {
  name: string;
  carrera: string;
  avatarColor: string;
};

export default function UserProfileSummary({
  name,
  carrera,
  avatarColor,
}: UserProfileSummaryProps) {
  return (
    <div className="user_profile">
      <div
        className="user_avatar"
        style={{ backgroundColor: avatarColor }}
        aria-hidden="true"
      >
        {name.trim().charAt(0).toUpperCase()}
      </div>
      <div className="user_profile_info">
        <h2>{name}</h2>
        <p>{carrera}</p>
      </div>
    </div>
  );
}

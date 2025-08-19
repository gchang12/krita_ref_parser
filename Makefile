_server:
	xfce4-terminal --working-directory=/home/eclair/Documents/coding/_web-dev/kritaref_palette/frontend/kritaref_palette/ &
	printf '\033]0;%s\007' "react-server";
	cd frontend/kritaref_palette/ && npm run dev -- --open --port 3000;

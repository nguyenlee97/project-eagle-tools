# Eagle — Phòng thử skin

Mở **http://127.0.0.1:8943/** sau khi chạy `Start-Viewer.ps1` trong thư mục này. Có thể chạy trực tiếp `node server.mjs`. Server chỉ lắng nghe trên máy này; không cần mạng để dùng viewer sau khi đã cài dependency.

## Thư viện và dữ liệu đánh giá

- Kho cá thể: `C:\Users\LENOVO\Desktop\GTA\Skin Library\Project Eagle\numbered-skins`.
- `catalog.json`: một khóa ổn định cho mỗi cặp DFF/TXD khác byte; nhiều bản tải giống byte dùng chung cá thể và giữ các nguồn gốc. Khóa/ID nội bộ giữ liên kết với đánh giá, không dùng số thứ tự làm tên hiển thị chính. Dữ liệu cá thể có series, nhóm cũ, mức cũ, link nguồn và tình trạng tài nguyên.
- `raw\Tên nhân vật__hậu-tố.dff` và `.txd`: tên gợi nhớ kèm hậu tố khóa để không trùng tên khi gom chung. Chủ yếu là **hardlink cùng ổ C**, nên tên mới không tạo thêm bản sao dữ liệu. Không sửa nội dung các file này: chỉnh một hardlink cũng chỉnh file gốc. Công cụ tối ưu sau này phải tạo bản sao trước khi sửa.
- DFF không tìm được TXD vẫn có ID, hiện geometry không texture và cảnh báo. Không tự ghép bừa TXD vào DFF. Các mục chỉ giữ metadata có ID nhưng không có file trong `raw`.
- `npcs.json` và `npc-assets`: 1.638 slot NPC trong cấu hình Eagle đang chọn và tài nguyên lấy từ IMG đang được khai báo. Đây là dữ liệu để xem/đối chiếu, không phải bản cài mod.
- `reviews.json`: phần đánh giá/ghi chú riêng của từng cá thể. Mức đang dùng = mức chấm riêng nếu có, nếu không thì kế thừa mức cũ trong catalog (Thích / Hơi thích / Bình thường). Rất thích chỉ có khi chấm riêng; thêm ghi chú hoặc cờ không làm mất mức kế thừa. Nút Dùng mức cũ xóa mức ghi đè riêng. Không sao chép hàng nghìn mức cũ vào file đánh giá riêng. Được ghi nguyên tử sau mỗi thay đổi; `review-changes.jsonl` giữ lịch sử thay đổi. Nút **Xuất đánh giá** tạo bản JSON mang theo được; **Nhập JSON** nhập lại đánh giá cá thể của viewer này.
- `mappings` trong file đánh giá là bản nháp NPC ID → skin key. Đánh dấu Không sử dụng sẽ bỏ các bản nháp gán skin đó. Chỉ nút **Áp dụng bản build / Phục hồi** mới đổi archive game; đánh giá, gán và import không tự cài skin.

## Gán skin và build vào game

1. Chọn NPC bên phải, chọn skin bên trái, bấm **Gán skin đang xem**. Lặp lại cho các slot cần thay.
2. Mở **Build & áp dụng vào game** dưới phần đánh giá. Xem danh sách gán rồi bấm **Build IMG từ bản nháp**.
3. Tắt game và bấm **Áp dụng bản build**. Khởi động lại game để kiểm tra. Sau áp dụng, khung NPC hiển thị skin đã áp dụng qua viewer; đây không phải nghiệm thu rig/animation trong game.
4. Đổi/bỏ gán rồi build và áp dụng lại để cập nhật. Bỏ gán sẽ trả slot đó về bản nền trước lần build đầu của viewer. **Phục hồi trước viewer** trả toàn bộ archive do viewer quản lý về bản nền đó, giữ bản nháp để dùng lại.

Eagle hiện tắt `gta3.std.stream`, nên tính năng này thay đúng member trong IMG đã mount, không dựa vào loose-file overrides hay tự sửa IDE. Đọc lại `default.dat`, `gta.dat`, `peds.ide` và chỉ mục IMG ở mỗi lần build. Từ chối member trùng ở nhiều archive, nguồn thiếu/hỏng header, skin bị loại và slot không khớp IDE. Khi các NPC dùng chung TXD được gán skin có texture khác nhau, builder giữ texture nền, ghép thêm các texture PC D3D8/D3D9 và đổi tên texture cùng tham chiếu material của DFF trong bản build để tránh đụng tên. NPC chưa gán tiếp tục dùng texture nền; DFF/TXD trong thư viện, geometry, rig và IDE không bị sửa. MatFX có tham chiếu texture riêng hoặc định dạng không hỗ trợ sẽ bị từ chối rõ ràng. Nếu tất cả NPC dùng chung đã được gán cùng nội dung TXD, builder dùng trực tiếp TXD đó.

`numbered-skins/deployment/baseline` giữ snapshot byte-for-byte của archive đang cài ở lần viewer build đầu (bao gồm mod đã có trước đó). `build.json` giữ manifest và hash. Mỗi lần build xuất phát từ baseline, chỉ giữ một thế hệ candidate thành công; IMG không phình dần qua các lượt build. Kiểm tra toàn bộ prefix ngoài 8 byte metadata của mỗi directory entry được chọn và hash payload mới. Mỗi member tối đa 65.535 sector × 2.048 byte.

`deployment/settings.json` có thể đặt `buildRoot` sang ổ khác để tạo IMG lớn; hiện dùng `D:\GTA Staging\Project Eagle Viewer Builds`. Baseline và manifest vẫn ở thư viện. Kiểm tra chỗ trống trước build và áp dụng; tiến trình build hiển thị số member đã ghi và giai đoạn đối chiếu hash. Build chỉ tạo candidate, không cài vào game. Cần giữ ổ chứa candidate kết nối cho tới khi áp dụng hoặc build lại; nguồn DFF/TXD gốc và các file ghép đều được kiểm hash trước áp dụng.

Khung **Mapping → Build IMG → Áp dụng vào game** chia ba bước với số lượng nháp/đã áp dụng và nhãn bản build cũ khi nháp thay đổi. Nhập hoặc dán **Thư mục lưu IMG** rồi bấm **Lưu đường dẫn**; nhận đường dẫn tuyệt đối, kiểm tra quyền ghi và dung lượng trống, từ chối lưu trực tiếp trong thư mục game. Đổi đường dẫn chỉ áp dụng cho lượt build tiếp theo, không di chuyển candidate cũ. Đường dẫn đang sửa chưa lưu sẽ khóa nút Build.

Đọc DFF khi ghép TXD chung hỗ trợ cùng trường hợp độ dài Struct/Clump có bit `0x01000000` như reader preview: chỉ nhận diện khi độ dài khai báo vượt toàn bộ file, sau đó vẫn kiểm tra giới hạn chunk cha. Bản build ghi độ dài chuẩn; giữ nguyên payload geometry, rig và plugin. TXD vẫn kiểm tra độ dài nghiêm ngặt. Lỗi ghép ghi tên TXD chung và file/NPC liên quan. Đã đối chiếu hai cặp Ellen ZZZ/BW CONSTRUCT2 ngày 22/10: geometry và số material nhận texture giữ nguyên trước/sau khi tách tên; chưa thay thế kiểm tra trong game.

Từ bản sửa crash 22/10, builder còn chuyển DFF PC RW 3.3.0.2 sang wire format SA 3.6.0.3 trong candidate, gồm geometry surface properties và Skin plugin legacy; không chỉ đổi version tag. Native TXD D3D8 DXT1/3/5 được chuyển header sang D3D9, giữ nguyên byte mip. File gốc, catalog, ranking và mapping được giữ. Các kiểu cũ chưa hỗ trợ bị từ chối rõ ràng. Manifest build ghi `compatibilityConversions` và tiếp tục kiểm hash nguồn gốc trước áp dụng. [Bằng chứng và kiểm tra bản sửa](../../docs/project-eagle/crash-sa-ped-compatibility-2026-10-22.md).

**Xóa toàn bộ mapping nháp** có xác nhận ngay trong khung và lưu mapping trước khi xóa tại `deployment/mapping-backups/*.json`. Giữ đánh giá, file skin, hai pool và tài nguyên đã cài; xóa preview/undo của lượt trộn cũ để tránh khôi phục nhầm nháp vừa bỏ. Nếu mapping đổi sau khi mở xác nhận, thao tác bị từ chối (409) để tải lại trước khi xóa. Đây là nút để người dùng chủ động dùng, không tự xóa khi cập nhật tool.

Áp dụng kiểm tra game đã tắt, mapping/config/source còn khớp build, hash archive chưa đổi bên ngoài viewer; chuẩn bị đủ file thay thế trước khi đổi archive, giữ rollback cùng thư mục rồi kiểm hash sau cài. Khi lỗi ghi, cố phục hồi giao dịch. Nếu tác vụ bị ngắt/mất điện, nút **Phục hồi tác vụ bị ngắt** chỉ hiện khi có journal/lock; không ghi đè file có hash lạ. Không tự tải game hay xóa save. Không sửa audio, Aether, population hoặc script.

## Nhập thêm skin

Nút **+ Nhập skin** nhận nhiều file `.dff/.txd` hoặc pack `.zip/.rar/.7z`. Chọn series có sẵn hoặc **+ Tạo series mới**, chọn Rất thích / Thích / Hơi thích / Bình thường, có thể ghi link nguồn. Bấm **Phân tích file** để xem danh sách cặp rồi **Nhập các cặp đã chọn**. Series/mức áp dụng cho các skin mới trong lượt nhập; mức được lưu là đánh giá riêng. Cặp trùng byte giữ nguyên metadata và đánh giá hiện có, không ghi đè.

Giải nén qua 7-Zip chỉ lấy DFF/TXD và archive lồng (tối đa 4 tầng); không chạy script đi kèm. Ghép cùng thư mục/tên trước, trường hợp TXD duy nhất có cảnh báo để xem lại. Trường hợp còn mơ hồ/thiếu file nằm ngoài danh sách được nhập, không ghép tùy tiện. Archive có mật khẩu cần giải nén thủ công trước. Giới hạn mỗi lượt: 2.000 file đầu vào, 1 GiB/file, 4 GiB upload; tối đa 20.000 member và 8 GiB giải nén. Header RenderWare/CRC và hash được kiểm tra; điều này chưa thay thế kiểm tra rig/texture trong game.

File nhập có tên gợi nhớ + khóa chống trùng trong `raw`; session ghi provenance tên gốc. Upload/giải nén tạm được dọn sau commit, các hardlink của cặp được chọn vẫn giữ dữ liệu. Catalog và đánh giá có journal phục hồi khi server khởi động lại; không mất đánh giá cũ. Trong lúc tác vụ chạy, các điều khiển sửa dữ liệu được tạm khóa để tránh thay đổi giữa chừng.

## Bổ sung TXD và quy tắc dung lượng

Trong khung skin, **Bổ sung / thay TXD** nhận một file TXD tối đa 128 MiB. Tool kiểm tra header, giải mã texture, đối chiếu tên texture được DFF yêu cầu trước khi cho ghép. File lỗi hoặc không khớp bất kỳ vật liệu nào bị chặn; khớp một phần có danh sách còn thiếu để cân nhắc. Tên file bên ngoài không cần giống DFF. Giữ nguyên ID/key đánh giá và ghi lại `contentKey` của cặp byte mới; giữ lịch sử TXD cũ, mapping và nguồn. Không đổi game cho tới khi build/áp dụng lại. Sau ghép, dung lượng, bộ lọc thiếu TXD và cờ tự động được tính lại. Upload/commit dùng journal như import; DFF hoặc skin đã đổi giữa lúc kiểm tra và ghép sẽ bị từ chối.

Quy tắc tổng **DFF + TXD > 10 MiB**: Bình thường → Không sử dụng, lý do `vượt ngưỡng dung lượng 10 MiB`; Thích/Hơi thích → Cần tối ưu; Rất thích/không rõ mức → không thêm cờ tự động. Tính theo mức đang dùng (riêng trước, kế thừa sau), áp dụng khi chấm/lấy lại mức cũ, nhập JSON, import skin và bổ sung TXD. `manualFlags` giữ quyết định thủ công, `autoSizePolicy` ghi cờ phát sinh từ quy tắc; khi đổi ranking chỉ cờ tự động cũ được gỡ. Bật/tắt cờ tay không vô hiệu hóa quy tắc đang có hiệu lực. Quy tắc không phải cờ nội dung tình dục hóa trẻ vị thành niên và không chặn preview.

Ngày 18/10 đã dọn 116 mục khỏi danh sách (3 lỗi preview, 66 không Skin plugin, 6 vũ khí/phụ kiện khác, 41 bản trùng sau khi lọc các nhóm trên), còn 3.120. Trùng = tên hiển thị chuẩn hóa + đúng số byte DFF và TXD; giữ record có mức hiệu lực cao nhất, gộp nguồn/ghi chú và chuyển mapping nháp. Đây không phải khẳng định hai file cùng size có byte giống nhau. Snapshot danh mục/review và các raw link được chuyển vào `maintenance/*-cleanup/`; `catalog-dispositions.json` ngăn importer cũ đưa mục đã bỏ quay lại. Không xóa archive và kho nguồn. Các ngoại lệ ped được người dùng xác nhận có `classificationOverride`; ba mẫu `sasuke1`, `sakura1`, `kakash1` có bộ lọc Cần kiểm tra UV/vật liệu, vẫn giữ lại chờ đánh giá.

Bộ lọc kết hợp: game/anime, nhóm cũ (yêu thích / skin cũ / skin nhỏ / skin pack), mức hiệu lực hoặc chỉ mức cũ/riêng, tình trạng thiếu file/texture/lỗi viewer, thiếu nguồn hoặc series. Link nguồn mở trực tiếp từ khung xem; nguồn không nối được có nhãn rõ và có đường dẫn file gốc, không tạo URL phỏng đoán.

Các lựa chọn: **Rất thích / Thích / Hơi thích / Bình thường**. Hai cờ **Cần phân tích tối ưu dung lượng** và **Không sử dụng** tách riêng khỏi mức thích. Không tự suy ra tần suất, vùng hay quyết định cài từ mức đánh giá. Mức cũ Không chọn trước đây được giữ riêng để lọc; không tự biến thành cờ vi phạm policy của đánh giá mới.

Kéo chuột trái để xoay, chuột phải để dịch góc nhìn, lăn để zoom. Có tự xoay, khung lưới, đặt lại góc và chụp ảnh. Mũi tên trái/phải chuyển skin; phím 1–4 chọn mức đánh giá. Vị trí đang xem được nhớ trong trình duyệt, đánh giá được giữ trong file độc lập với trình duyệt. Chọn đánh giá không cuộn lại đầu trang.

Dung lượng hiển thị là **DFF + TXD sau giải nén**, dùng KiB/MiB (1 MiB = 1.048.576 byte). Cặp dùng chung một TXD vẫn có dung lượng đầy đủ khi tính riêng; tổng dung lượng cặp không bằng dung lượng vật lý sau hardlink/chia sẻ file.

## Chỉnh preview riêng từng skin

Dưới mỗi khung 3D có **Chỉnh hiển thị: màu / ánh sáng / alpha**. Có thể chọn có ánh sáng hoặc texture không ánh sáng, bật/tắt màu đỉnh và màu vật liệu DFF, chỉnh độ sáng, tính lại normals để xem và đổi ngưỡng cắt alpha. Mặc định tắt màu đỉnh để tránh các skin có prelight đen bị nhân tối lên texture. Nút **Xem màu texture gốc** tắt ánh sáng và hai lớp màu nhân; **Mặc định skin/NPC này** chỉ xóa lựa chọn của mẫu hiện tại.

Thiết lập lưu theo skin key (NPC theo ID và skin đã áp dụng) trong localStorage `eagle-viewer-display-v1` của trình duyệt này, độc lập từng khung. Chuyển skin hoặc tải lại trang sẽ lấy lại lựa chọn đã lưu. Không ghi vào ranking, DFF/TXD, bản build hay tài nguyên game; xuất JSON đánh giá không mang theo thiết lập trình duyệt. Chỉnh trực tiếp trên model hiện tại, không tải/giải nén lại texture cho mỗi thao tác.

## Giới hạn và nguồn bằng chứng

Đợt tối ưu 22/10/2026 dùng `optimize-library-batch.mjs` và ghi nhật ký có thể tiếp tục trong `staging/project-eagle/texture-optimization-2026-10-22`. `backup-optimization-inputs.mjs` đọc manifest snapshot 18/10 trên D, kiểm hash backup có sẵn và chỉ chép object còn thiếu sang `D:/Skin Backup/Optimization-2026-10-22`. Bản tối ưu là record/phiên bản mới, không ghi vào hardlink gốc. API add-version giữ series, nguồn, ranking và mapping; provenance `optimization` nối source hash, candidate hash và báo cáo kiểm tra. Nhóm **Tối ưu TXD** lọc các bản mới; nhãn **Đã nén TXD** khác cờ còn cần phân tích. Cờ thủ công và policy >10 MiB tiếp tục được giữ/tính như trước.

TXD dùng chung được nén một lần theo SHA-256. DXT1 cho raster hoàn toàn opaque, DXT5 khi có alpha; giữ resolution/tên/thứ tự và số mip; texconv tái sinh các mip phụ khi chuyển raster. Raster đã nén không nén lại. Đệm zero sau dictionary được giữ, tail có dữ liệu khác zero bị từ chối. Bộ kiểm tra ảnh giữ lại mẫu PSNR RGB <32 dB hoặc alpha RMSE >4 hay >0,1% pixel đổi phía ngưỡng alpha 128. Mỗi DFF còn được parser đọc cùng TXD mới và kiểm hash nguồn; asset không đạt không được ép nhập. Đây là sàng lọc tự động, không thay nghiệm thu trong game.

Lệnh: `node optimize-library-batch.mjs compress <staging>` rồi `node optimize-library-batch.mjs register <staging>`; sổ nén và sổ nhập tách riêng để có thể chạy chồng nhau sau khi backup đầu vào hoàn tất. `backup-optimized-output.mjs` lưu TXD mới lên D; `finalize-texture-batch.mjs` kiểm nguồn/mapping/IMG và tạo báo cáo cuối. Không tự build/apply trong batch. Chi tiết kết quả ở `docs/project-eagle/texture-optimization-2026-10-22.md`.

Từ 21/10/2026, mục **Phân phối skin ngẫu nhiên** có hai pool lưu trong `reviews.json` (`distribution`), đi cùng bản nháp mapping. Bộ lọc skin thêm giới hạn **nhỏ hơn N MiB** tính tổng DFF+TXD sau giải nén, và trạng thái đã/chưa gán của đúng phiên bản. Nạp kết quả lọc lấy tất cả item trên mọi trang; mặc định lấy một đại diện khớp/item, có checkbox lấy mọi phiên bản khớp. Nút nạp bản đang xem chọn đúng phiên bản hiện tại. Nạp lại giữ thêm các lượt trùng để tạo trọng số. Skin thiếu DFF/TXD hoặc bị loại không được nạp; cờ tối ưu không ngăn nạp.

NPC có bộ lọc nhóm, khu vực cụ thể, ưu tiên Vice City/Carcer City/Los Santos (403 ID theo cấu hình hiện tại), và đã/chưa gán trong bản nháp. Có 6 slot bạn gái được xác định bằng ID/model trong IDE. Ngoài đường là ứng viên population; có thể trong nhà là suy luận từ cohort/địa điểm, không phải xác nhận spawn. Nhóm giao nhau và mục Chưa rõ được giữ riêng. Bằng chứng: `docs/project-eagle/npc-filter-categories-2026-10-21.md`.

Hai pool có option chỉ nạp chưa gán hoặc gồm đã gán. NPC được khử trùng ID. **Trộn thử** xáo thứ tự skin và NPC, tùy chọn lặp lại pool khi thiếu; khi lặp mỗi vòng dùng hết các lượt trước khi xáo vòng mới. Kết quả xem trước ghi số overwrite và mục bị bỏ qua. **Lưu kết quả vào bản nháp** lưu toàn bộ mapping một lần; không thay game. Mỗi lần lưu có một lượt hoàn tác, từ chối ghi đè nếu một slot vừa được sửa tiếp. Bản trộn cũ bị từ chối nếu mapping hoặc pool đã đổi; skin bị loại được kiểm tra lại lúc lưu. Các lượt chỉ-chưa-gán được kiểm tra lại khi trộn. NPC dùng chung TXD sẽ có cảnh báo; Build vẫn kiểm tra xung đột trước khi tạo IMG (hiện #49229 và #49236 dùng chung `lcs_chauff.txd`).

Kiểm tra mở rộng: `node --test distribution.test.mjs distribution-api.test.mjs npc-filters.test.mjs`. Các API pool qua `/api/distribution`, dùng chung hàng đợi ghi với review/mapping và bị chặn trong tác vụ import/repair/deployment. Kiểm thử UI riêng đã nạp 212 item trên nhiều trang thành 424 lượt/212 phiên bản, trộn/lưu 403 NPC, kiểm tra filter đã gán rồi hoàn tác về 0. Không thực hiện mapping thử trên thư viện chính.

Viewer dựng mô hình tĩnh với texture gốc, không chạy GTA hay kiểm thử hoạt ảnh/rig. Hướng đứng được căn theo trọng tâm vùng đầu/cổ và bàn chân nếu có trọng số xương GTA phù hợp; đây là hỗ trợ xem, không thay đổi DFF. Các lỗi đọc model, thiếu texture hoặc texture vượt ngân sách xem sẽ hiện cảnh báo; không có nghĩa đã thử và hỏng trong game. Mỗi khung giữ một model; khi đổi skin, geometry/texture cũ được giải phóng. Không sinh thư viện PNG/GLB hàng loạt. DFF/TXD được xử lý trong Web Worker; quá 15 giây thì dừng mẫu đó và vẫn có thể tiếp tục đánh giá/chuyển mẫu khác. Giới hạn xem: DFF 128 MiB, tối đa 64 triệu pixel texture giải mã cho một TXD; vượt giới hạn cần phân tích riêng.

NPC: các nhóm, khu vực và số lần model có mặt trong danh sách lấy từ file cấu hình. Tỉ trọng phần tử trong nhóm **không phải xác suất spawn**. Không có tọa độ/đường cụ thể nếu cấu hình hiện có không nối được đến model. Có nhãn phân biệt tài nguyên/cấu hình với việc người dùng đã thử trong game.

Những mẫu đã được xác định thuộc nội dung tình dục hóa trẻ vị thành niên chỉ có bản ghi Không sử dụng; không giải nén bổ sung, đưa vào thư mục raw hay gửi cho renderer. Bản gốc không bị xóa. Các lỗi kỹ thuật hoặc khác tên nội bộ không tự động loại khỏi kho.

Backup `D:\Skin Backup\Project Eagle-2026-10-18` là snapshot được kiểm tra trước khi tạo viewer. Các file đánh giá, danh mục đánh số và phần xuất NPC mới chưa tự động thêm vào snapshot đó; dùng Xuất đánh giá để có bản độc lập.

## Tái tạo và kiểm tra

Cập nhật từ `Downloads/fix`: 52 skin được ghép TXD, thêm 11 biến thể texture có key/ID riêng. Các phiên bản TXD người dùng yêu cầu giữ đủ được so bằng contentKey/hash, không bị ẩn chỉ vì cùng dung lượng. Cờ `explicitTextureVariants` cũng bảo vệ chúng khỏi quy tắc dọn trùng theo size cũ. `textureVariant` giữ nhãn và đường dẫn nguồn; DFF được dùng lại, không nhân bản geometry.

Thanh **Phiên bản N / tổng** luôn hiện phía trên model, có dropdown và nút Trước/Sau. Gán bằng nút xanh ngay cạnh selector dùng chính key của bản đang xem, độc lập với bản đại diện. Trạng thái mapping ghi rõ ID phiên bản và nhãn TXD. Đổi bản đang xem không tự thay mapping đã lưu. Các bản Rất thích vẫn đứng riêng trong danh sách nhưng selector có thể mở các bản liên quan cùng family. Mẫu chưa có TXD không được gán qua nút UI.

Trong hộp Bổ sung TXD, chọn **Ghép / thay TXD** hoặc **Thêm phiên bản mới, giữ bản đang xem**, kèm tên phiên bản tùy chọn. Đã có TXD thì mặc định là thêm phiên bản. API commit nhận `mode=add-version`; kiểm tra header/texture/hash và journal như thao tác ghép thường. Cặp cùng hash DFF+TXD đã tồn tại không tạo bản mới. Thêm phiên bản không tự đổi mapping cũ.

Ngoại lệ khi dọn nhóm thiếu TXD ngày 18/10: 85 record trong 29 cụm được gắn `versionFamily` theo cùng hash archive giải nén và cùng tên, gồm biến thể đuôi `2` nếu tên gốc cũng có trong chính archive đó. Các cụm này giữ chung dù tổng size lệch quá 5% do thiếu TXD hoặc DFF khác chế độ hiển thị; ghép TXD sau đó không làm tách cụm. Không gom xuyên archive chỉ vì tên giống. Rất thích vẫn đứng riêng. Hai bản chưa có TXD chỉ được ẩn trùng khi cùng cụm, cùng số byte DFF và cùng trạng thái thiếu TXD; không coi chúng là trùng bản đã có TXD. Dropdown ghi rõ tên từng bản và Thiếu TXD. Chi tiết: `docs/project-eagle/unpaired-skin-families-2026-10-18.json`.

Từ 18/10, danh sách gom cùng tên hiển thị (chuẩn hóa Unicode, khoảng trắng đầu/cuối và hoa/thường) khi tổng DFF+TXD lớn nhất không vượt 1,05 lần bản nhỏ nhất trong cụm. Không nối dây chuyền qua nhiều bản để vượt ngưỡng. Mức hiệu lực **Rất thích** đứng riêng và tự tách ngay khi chấm; bản chỉ giữ metadata cũng đứng riêng. Cùng đúng cả số byte DFF và TXD chỉ hiện một phiên bản, giữ bản điểm cao nhất; đây là tiêu chí dung lượng do người dùng chọn, không phải kiểm chứng hash giống nhau. Cặp chưa có TXD không bị coi như TXD 0 byte để xóa trùng.

Dropdown **Phiên bản đang xem** cho đổi bản trong item. Mặc định dùng bản điểm cao nhất (mức riêng → cũ; hòa điểm chọn ổn định theo key). Nút **Dùng bản này làm đại diện** lưu vào `numbered-skins/version-preferences.json`. Bộ lọc khớp bất kỳ phiên bản nào trong cụm; nếu đại diện không khớp, danh sách hiển thị bản khớp điểm cao nhất. Mỗi phiên bản vẫn giữ key, đánh giá, cờ, nguồn và mapping riêng; gán NPC dùng đúng phiên bản đang xem. Gom item không xóa/đổi tên file hoặc chuyển mapping sang bản khác. Các cụm được tính lại khi chấm, nhập skin hoặc ghép TXD.

Ghép TXD giữ nguyên từ khóa, series, nhóm, ranking, tình trạng, exclude, sort, trang và vị trí cuộn danh sách (trang được giới hạn nếu số kết quả giảm). Nếu lựa chọn tình trạng không còn kết quả, vẫn giữ option `(0)`. Skin vừa sửa vẫn nằm trong khung xem dù đã ra khỏi tập kết quả. **Xóa bộ lọc** là thao tác chủ động của người dùng.

`recover_metadata.py` phục hồi nguồn cho các DFF lẻ từ báo cáo điều tra exact-key. Mặc định chỉ dry-run, `--write` tạo snapshot catalog rồi thêm trường `provenanceRecovery`; không sửa review, tài nguyên hoặc tự chọn TXD. `enrich_catalog.py` giữ lại các bằng chứng phục hồi này trong các lần enrich tiếp theo.

Chạy từ thư mục công cụ:

```powershell
C:\Python310\python.exe -X utf8 import_catalog.py --no-extra-inspection
C:\Python310\python.exe -X utf8 enrich_catalog.py --write
C:\Python310\python.exe -X utf8 name_assets.py
C:\Python310\python.exe -X utf8 import_npcs.py
node validate_models.mjs
node validate_meshes.mjs
node --test server.test.mjs review-model.test.mjs skin-import.test.mjs textures.test.mjs preview-settings.test.mjs size-policy.test.mjs txd-repair.test.mjs skin-versions.test.mjs
C:\Python310\python.exe -X utf8 -m unittest test_deploy_skins -v
```

Không xóa catalog/id map trước khi nhập thêm: chúng giữ ID và liên kết với đánh giá. Đọc báo cáo importer trước khi xử lý archive thiếu mật khẩu, hỏng hoặc vượt giới hạn; không coi một archive đã tải là đã giải nén thành công.

### Sửa nhóm / game-anime

Nút **Sửa nhóm / game-anime** dưới model cho bỏ nhóm cũ bằng ×, chọn tên có sẵn hoặc nhập tên mới rồi Thêm. Sửa độc lập nhóm và game/anime, có thể giữ nhiều tên hoặc bỏ hết. Mặc định chỉ sửa phiên bản đang xem; chọn **Cả item hiện tại** để thay danh sách nhóm/series cho toàn bộ record trong item đó, gồm bản trùng đang ẩn. Những item Rất thích đứng riêng không bị kéo theo từ family. Hộp thoại ghi rõ số record chịu ảnh hưởng.

Các chỉnh sửa lưu nguyên tử vào `numbered-skins/group-overrides.json`, có nhóm ban đầu và lịch sử trước/sau để truy vết. API catalog, export, import và pool đọc liên kết đã sửa; enrich/rebuild catalog không ghi đè lựa chọn này. File đánh giá JSON xuất từ nút cũ chỉ kèm tên nhóm đã giải quyết trong `resolvedRatings`, **không thay thế bản backup group-overrides.json**. Giữ file này cùng catalog và reviews khi sao lưu thư viện. Không sửa ranking, nguồn, file DFF/TXD hoặc mapping NPC. Lưu giữ bộ lọc/trang/vị trí cuộn và góc 3D; skin đang xem có thể nằm ngoài kết quả lọc sau khi chuyển nhóm. Nếu item hoặc nhóm đã đổi khi hộp thoại đang mở, API từ chối lưu dữ liệu cũ (409); mở lại hộp thoại trước khi sửa tiếp.

Kiểm tra: `node --test skin-groups.test.mjs server.test.mjs skin-versions.test.mjs review-model.test.mjs`.

### Nhập nhiều cặp DFF/TXD

Tùy chọn **Cho phép nhập trùng với skin đã có** mặc định tắt. Bật để tạo item riêng với key, nhóm và đánh giá riêng, giữ nguyên item gốc; không tự gom bản mới với bản gốc theo tên/size. Ô **Thêm vào nhóm** chọn tên sẵn có hoặc tạo nhóm mới cho cả lượt nhập. Cùng một cặp xuất hiện nhiều lần trong chính một lượt vẫn chỉ tạo một item; nhập lại ở lượt tiếp theo có thể tạo thêm bản. `contentKey` giữ hash cặp gốc để chế độ mặc định vẫn nhận diện được trùng. Hai bản trùng qua importer có thể dùng chung đường dẫn tài nguyên đã lưu, nhưng đánh giá và mapping độc lập. File vẫn được kiểm tra định dạng/ghép cặp; bản đã giữ chỉ metadata không được sao chép để bỏ qua trạng thái đó.

Trong **+ Nhập skin**, giữ Ctrl/Shift để chọn nhiều file DFF/TXD hoặc pack; chọn tiếp lần nữa sẽ thêm vào danh sách đang chờ thay vì thay thế nó. Danh sách ghi tên, size và tổng số DFF/TXD/pack, cho bỏ riêng từng file hoặc bỏ hết lựa chọn. Chưa bấm Nhập thì chưa có skin nào được thêm vào catalog. Nếu sửa danh sách sau khi phân tích, preview cũ bị ẩn và phải phân tích lại.

**+ Thêm thư mục** lấy file trong các thư mục con và giữ đường dẫn tương đối. Nhờ đó `Skin A/skin.dff` chỉ ghép với TXD của thư mục Skin A, không ghép nhầm sang `Skin B/skin.txd`. Ưu tiên tên cùng stem trong cùng thư mục; nếu thư mục chỉ có một TXD thì giữ cơ chế fallback có cảnh báo. Cặp chưa ghép được được liệt kê để xem lại; không tự ghép theo thứ tự chọn file. Series và ranking áp dụng chung cho toàn bộ lần nhập. Giới hạn hiện tại: 2.000 file, tổng 4 GiB và tối đa 1 GiB mỗi file. File đã chọn trùng tên/size/ngày sửa không được thêm lặp vào hàng chờ. File ngoài DFF/TXD/ZIP/RAR/7Z và file rỗng bị bỏ qua khi chọn cả thư mục. Kiểm tra nhiều cặp rời và tên file giống nhau ở thư mục khác nhau nằm trong `skin-import.test.mjs`.

Renderer dùng Three.js 0.170.0 và [DFF-Loader 1.0.1](https://github.com/jackal1337/DFF-Loader), giấy phép MIT giữ trong `node_modules` / `vendor/dff-loader/LICENSE`. Bản vendor đã sửa lựa chọn decoder theo D3D9 format, xử lý mask texture, bỏ tải ảnh fallback ngoài TXD, thêm kiểm tra biên và ngân sách bộ nhớ. Phiên bản dependency được khóa trong package-lock.json.


### Hướng đứng và hướng mặt khi preview

Viewer tự nhận hướng người từ các đỉnh gắn vào xương đầu/jaw, bàn chân/toe và hai bên tay/vai. Bàn chân 43/53 được xét cùng toe 44/54 vì nhiều model không có đỉnh gắn vào toe. Nếu cả foot/toe đều không có đỉnh được gắn, lần lượt dùng bắp chân 42/52 rồi đùi 41/51; Komugi #327 thuộc trường hợp bắp chân. Fallback này không thay kết quả của các mẫu đã có foot/toe. Hướng hai bên tay giúp phân biệt mặt trước/sau; nếu chỉ tìm được đầu/chân thì chỉ dựng đứng, còn thiếu thông tin sẽ giữ hướng cũ. Đối chiếu parser cho Barbara #2157, Bronya HSR #2523, girl1 #494 và Dori #1145 đều nhận đủ các hướng và có chiều cao theo Y sau sửa.

Trong **Chỉnh hướng / màu / ánh sáng / alpha**, có bật/tắt tự dựng, xoay X/Y/Z theo bước 90° và nút **Đặt lại hướng tự động**. Giữ Y=180° để đổi mặt trước/sau; X hoặc Z=±90° để dựng các bản nằm dọc/ngang. Thiết lập nhớ theo key skin hoặc NPC trong localStorage hiện có. **Đặt lại góc** chỉ đặt camera; **Đặt lại hướng tự động** chỉ đặt hướng người; preset màu texture giữ hướng đang chỉnh. Xoay lại sẽ tính từ model ban đầu, không cộng dồn, và luôn kê đáy model lên mặt sàn. Chỉ đổi preview, không sửa DFF/TXD, rig, đánh giá hay mapping trong game.

Mapping hiển thị hai chiều: từng item / phiên bản skin ghi ID và tên model NPC đã gán; khung skin liệt kê toàn bộ NPC của bản đang xem và mapping của các bản khác trong item. Dropdown NPC và thông tin ngay trên model NPC ghi tên skin mod, ID phiên bản và nhãn TXD. Khi NPC có bản đã áp dụng, thông tin Trong game được tách khỏi Nháp. Các nhãn cập nhật khi gán/bỏ gán, loại skin, nhập mapping JSON hoặc trộn pool; không thay đổi mapping khi chỉ xem thông tin.

### Tương thích rig VC khi build NPC SA

Sau bước chuyển wire format RW 3.3, builder nhận diện chính xác layout ped VC 24 khớp và chuyển sang thứ tự HAnim/Skin 32 khớp của SA bằng `sa_ped_rig.py`. Bước này cần thiết cả với `male01` vì game dùng model đó làm mẫu animation chung. Giữ nguyên mesh/UV/texture/trọng số và ma trận inverse-bind của các bone cũ, remap chỉ mục và thêm tám bone không gắn trọng số; bù local matrix khi đổi parent hai thigh để giữ bind-world transform. Đây là ngoại lệ có chủ đích với việc giữ nguyên FrameList trong bước chuyển wire format thuần túy. Chỉ thay bản dẫn xuất trong build; catalog, nguồn và mapping không đổi. Layout khác không được đoán cách retarget. Chi tiết và giới hạn nghiệm thu: `docs/project-eagle/crash-animation-rig-2026-10-22.md`. Kiểm tra: `python -m unittest test_sa_ped_rig test_sa_assets test_shared_txd test_deploy_skins`.

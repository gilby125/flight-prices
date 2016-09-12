# system, you should be using db:schema:load, not running all the migrations
# from scratch. The latter is a flawed and unsustainable approach (the more migrations
# you'll amass, the slower it'll run and the greater likelihood for issues).
#
# It's strongly recommended that you check this file into your version control system.

ActiveRecord::Schema.define(version: 20160911175013) do

  # These are extensions that must be enabled in order to support this database
  enable_extension "plpgsql"

  create_table "fares", force: :cascade do |t|
		t.string   "mapIdfrom"
		t.json	   "duration"
		t.json	   "return_duration"
		t.string	"flyto"
		t.json		"conversion"
		t.text		"deep_link"
		t.string	"mapidto"
		t.integer	"nightsindest"
		t.string	"_id_"
		t.string	"fly_duration"
		t.json		"countryto"
		t.json		"baglimit"
		t.integer	"atimeutc"
		t.integer	"price"
		t.string	"cityto"
		t.string	"flyfrom"
		t.integer	"dtimeutc"
		t.json		"countryfrom"
		t.integer	"dtime"
		t.text		"booking_token"
		t.string	"cityfrom"
		t.integer	"atime"
		t.json		"route"
		t.datetime "created_at",  null: false
		t.datetime "updated_at",  null: false
  end
  create_table "routes", force: :cascade do |t|
		t.integer	"route_atimeutc"
		t.string	"route_mapidfrom"
		t.string	"route_mapidto"
		t.string	"route_flightno"
		t.integer	"route_dtime"
		t.decimal	"route_latto"
		t.string	"route_flyto"
		t.integer	"route_return"
		t.string	"route_source"
		t.string	"route_id"
		t.string	"route_airline"
		t.decimal	"route_lngto"
		t.string	"route_cityto"
		t.string	"route_cityfrom"
		t.decimal	"route_lngfrom"
		t.integer	"route_atime"
		t.string	"route_flyfrom"
		t.integer	"route_price"
		t.decimal	"route_latfrom"
		t.integer	"route_dtimeutc"
		t.datetime "created_at",  null: false
		t.datetime "updated_at",  null: false
end
end
